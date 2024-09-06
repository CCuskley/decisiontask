const mainSocket=io()
var trialCount=0
var correctResps=0
var responses=[]
var responseDict={}
var keybinds={}
var taskStarted=false
var demoStartd=false
var trialStart,stimuliList;


function setStim(word) {
    trialStart=Date.now()
    $("#currentTarget").text(word)
}

mainSocket.on('connection confirmation', function(message) {
    console.log(message["data"])
});

mainSocket.on('randomized stimuli', function(message) {
    stimuliList=message["data"]
    setStim(stimuliList[trialCount]["name"])
    for (i=0;i<stimuliList.length;i++) {
        if (stimuliList[i]["status"]=="realAnimal") {
            $("#realAnimalList").append("<li>"+stimuliList[i]["name"]+"</li>")
        } else {
            $("#fakeAnimalList").append("<li>"+stimuliList[i]["name"]+"</li>")
        }
    }
});

mainSocket.on('human verified',function(message) {
    var isHuman=message["data"]
    if (isHuman==true) {
        $(".humanTestPrompt").hide()
        $(".taskInstructions").show()
        demoStarted=true
    } else {
        $(".humanTestPrompt").hide()
        $(".humanError").show()
    }
});

$("#agreeConsent").click(function() {
    mainSocket.emit('request stimuli')
    $("#formWrapper").hide()
    $("#instructions").show()
    var dice=Math.random()
    if (dice>0.5) {
        $(".realAnimalButton").text("D")
        $(".notAnimalButton").text("K")
        responseDict["buttonOrder"]="real_D;not_K"
        keybinds["d"]="realAnimal"
        keybinds["k"]="notAnimal"
    } else {
        $(".realAnimalButton").text("K")
        $(".notAnimalButton").text("D")
        responseDict["buttonOrder"]="real_K;not_D"
        keybinds["k"]="realAnimal"
        keybinds["d"]="notAnimal"
    }
    responseDict["keyBinds"]=keybinds
});

$("#checkHuman").click(function() {
    var theanswer=$("#humantest").val();
    mainSocket.emit('check human',{"data":theanswer});
});

$(".startTask").click(function() {
    $("#instructions").hide();
    $("#mainTask").show();
    taskStarted=true;
    demoStarted=false;
    trialStart=Date.now();
});

$(document).keypress(function (event) {
    var pressTime=Date.now();
    var key = event.key.toLowerCase()
    if ((key=="d" || key=="k") && (demoStarted || taskStarted)) {
        if (demoStarted) {
            $("#taskPrompt").slideUp()
            if (keybinds[key]=="realAnimal") {
                $(".goodTiger").show()
            } else {
                $(".badTiger").show()
            }
        }
        if (taskStarted) {
            var thisresp= {
                "trialNumber":trialCount,
                "target":stimuliList[trialCount]["name"],
                "targetType":stimuliList[trialCount]["status"],
                "rt":pressTime-trialStart,
                "response":keybinds[key],
                "responseKey":key
            }
            if (keybinds[key]==stimuliList[trialCount]["status"]) {
                correctResps+=1
            }
            responses.push(thisresp)
            trialCount+=1;
            if (trialCount>=stimuliList.length) {
                responseDict["responses"]=responses
                mainSocket.emit("store responses",{"data":responseDict})
                var propScore=Math.floor((correctResps/(trialCount+1))*100)
                $("#numRight").text(correctResps.toString())
                $("#numStims").text((trialCount+1).toString())
                $("#propRight").text(propScore.toString())
                $("#mainTask").hide()
                $("#endTask").show()
            } else {
                setStim(stimuliList[trialCount]["name"])
            }
        }
    }
});

$(".showScore").click(function() {
    $("#animalAnswers").fadeToggle()       
});

