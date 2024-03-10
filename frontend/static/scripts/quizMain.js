function LeaderBoard(onUse5050) {
  var used5050 = false;

  var joker5050 = document.getElementById("joker_5050");
  joker5050.addEventListener("click", function (event) {
    use5050();
  });

  this.setRank = function (rank) {
    console.log("Setting rank to " + rank);
    var r = document.getElementById("r_" + rank);
    if (rank > 1) {
      var rold = document.getElementById("r_" + (rank - 1));
      rold.classList.remove("marked");
    }
    r.classList.add("marked");
  }
  use5050 = function () {
    if (!used5050) {
      if (onUse5050()) {
        used5050 = true;
        document.getElementById("joker_5050").style.filter = "hue-rotate(90deg)";
      }
    }
  }


}

function Medallion() {
  var logo = document.getElementById("logo");
  var logoimg = document.getElementById("logoimg");
  var degrees = 0;
  var rotations = 0;
  var maxrotations = 0;
  var timeout = 0;
  var listener;
  this.lose = function (rank) {
    const amount = [0, 50, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000][rank - 1].toLocaleString();
    $("#lost").show();
    $("#lost-amount").text(amount);
    $("#lost-rank").text(rank);
    $("#lost button").click(function () {
      location.reload();
    });
  }
  this.win = function () {
    $("#won").show();
    $("#won button").click(function () {
      location.reload();
    });
  }
  this.rotate = function (l) {
    listener = l;
    rotations = 0;
    maxrotations = 360;
    timeout = 2;
    rot();
  }
  rot = function () {
    if (rotations < maxrotations) {
      rotations++;
      rotateOneDegree();
      window.setTimeout(rot, timeout);
    }
    else {
      listener();
    }
  }
  rotateOneDegree = function () {
    degrees += 1;
    if (degrees > 360) {
      degrees = degrees - 360;
    }
    logo.style.transform = "rotateY(" + degrees + "deg)";
    logo.style.webkitTransform = "rotateY(" + degrees + "deg)";
    logo.style.OTransform = "rotateY(" + degrees + "deg)";
    logo.style.MozTransform = "rotateY(" + degrees + "deg)";
  }
}

function Question() {
  this.rank;
  this.name;
  var answers = new Array();
  this.rightAnswer;
  this.setAnswers = function (ans, rightAnswer) {
    answers = shuffle(ans);
    for (i = 0; i < answers.length; i++) {
      if (answers[i] == rightAnswer) {
        this.rightAnswer = i;
      }
    }
  }
  this.getAnswers = function () {
    return answers;
  }
  shuffle = function (array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;
      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }
    return array;
  }
}

function QuestionBoard(ocl) {
  var ansElement = new Array();
  ansElement[0] = document.getElementById("ans1");
  ansElement[1] = document.getElementById("ans2");
  ansElement[2] = document.getElementById("ans3");
  ansElement[3] = document.getElementById("ans4");
  var onClickListener = ocl;
  var ansDiv = new Array();
  for (i = 0; i < 4; i++) {
    ansDiv[i] = document.getElementById("element" + i);
  }
  ansDiv[0].addEventListener("click", function (e) { click(0); });
  ansDiv[1].addEventListener("click", function (e) { click(1); });
  ansDiv[2].addEventListener("click", function (e) { click(2); });
  ansDiv[3].addEventListener("click", function (e) { click(3); });

  var questionElement = document.getElementById("question");
  this.newestQuestion;

  this.setQuestion = function (question) {
    this.newestQuestion = question;
    questionElement.innerHTML = this.newestQuestion.name;
    for (i = 0; i < 4; i++) {
      ansElement[i].innerHTML = this.newestQuestion.getAnswers()[i];
    }
  }
  this.right = function (pos) {
    ansDiv[pos].classList.remove("wrong");
    ansDiv[pos].classList.add("right");
  }
  this.wrong = function (pos) {
    ansDiv[pos].classList.remove("right");
    ansDiv[pos].classList.add("wrong");
  }
  this.clear = function () {
    for (t = 0; t < 4; t++) {
      ansDiv[t].classList.remove("right");
      ansDiv[t].classList.remove("wrong");
    }
  }

  click = function (pos) {
    onClickListener(pos);
  }
}

function getQuestionFromServer() {
  const p = new Promise((resolve, reject) => {
    $.ajax({
      url: "/question",
      type: "GET",
      success: function (response) {
        resolve(response);
      },
      error: function (xhr, status, error) {
        reject(error);
      }
    });
  });
  return p;
}

function getAllQuestions(questions_array) {
  const p = new Promise((resolve, reject) => {
    for (i = 0; i < 14; i++) {
      getQuestionFromServer().then((response) => {
        var q = new Question();
        q.rank = response.rank;
        q.name = response.question;
        q.setAnswers(response.answers, response.real_answer);
        questions_array.push(q);
        if (i === 14) {
          resolve(questions);
        }
      }).catch((error) => {
        reject(error);
      });
    }
  });
  return p;
}

function Game() {
  var questions = new Array();
  answerClick = function (i) {
    if (clickable) {
      check(i);
    }
  }

  randomIntFromInterval = function (min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }
  var medallion = new Medallion();
  var questionBoard = new QuestionBoard(answerClick);
  var leaderBoard = new LeaderBoard(function () {
    if (clickable) {
      var x = questionBoard.newestQuestion.getAnswers();
      var p1 = -1;
      var p2 = -1;
      while (p1 == -1 | p2 == -1) {
        var random = randomIntFromInterval(0, 3);
        if (questionBoard.newestQuestion.rightAnswer != random) {
          if (p1 == -1) {
            p1 = random;
          }
          else {
            if (random != p1) {
              p2 = random;
            }
          }
        }
      }
      questionBoard.wrong(p1);
      questionBoard.wrong(p2);
      return true;
    }
    else {
      return false;
    }
  });
  var rank = 1;
  var maxrank = 15;
  var clickable = true;

  check = function (i) {
    clickable = false;
    if (i == questionBoard.newestQuestion.rightAnswer) {
      questionBoard.right(i);
      rank++;
      if (rank <= maxrank) {
        medallion.rotate(function () {
          questionBoard.clear();
          clickable = true;
          console.log("New question");
          newQuestion(rank);
        });
      }
      else {
        medallion.win(function () {
          questionBoard.clear();
        });
      }
    }
    else {
      questionBoard.right(questionBoard.newestQuestion.rightAnswer);
      questionBoard.wrong(i);
      medallion.lose(rank);
    }
  }
  rank = 1;

  this.startGame = function () {
    console.log("Game started");
    newQuestion(rank);
  }
  newQuestion = function (rank) {
    console.log(questions);
    if (questions.length == 0) {
      $("#loading").show();
      getQuestionFromServer().then((response) => {
        console.log("Got new question");
        var q = new Question();
        q.name = response.question;
        q.setAnswers(response.answers, response.real_answer);
        leaderBoard.setRank(rank);
        questionBoard.setQuestion(q);
        if (rank > 1) {
          $("#loading").hide();
        }
        if (questions.length == 0) {
          getQuestionFromServer().then((response) => {
            $("#loading").hide();
            var q = new Question();
            q.name = response.question;
            q.setAnswers(response.answers, response.real_answer);
            questions.push(q);
            getAllQuestions(questions).then((response) => {
              console.log("Got all questions");
            });
          });
        }
      });
    }
    else {
      var question = questions.shift();
      console.log(question);
      questionBoard.setQuestion(question);
      leaderBoard.setRank(rank);
    }
  }
}

var game = new Game();
game.startGame();

