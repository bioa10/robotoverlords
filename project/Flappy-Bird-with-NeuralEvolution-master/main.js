document.onreadystatechange = function () {
  if (document.readyState === "complete") {
    canvas = document.getElementById("screen");
    ctx = canvas.getContext("2d");
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, setting.screen_w, setting.screen_h);
    ctx.fillStyle = "white";
    ctx.font = "30px Georgia";
    ctx.fillText("Flappy Bird", 120, 150);

    document.addEventListener("keydown", keyPress);

    document.getElementById("load-bird").addEventListener("click", loadbird);
    document.getElementById("train-bird").addEventListener("click", trainbird);

    brain_structure = [3, 4, 4, 2];

    pop_size = 100;
    keep_size = 10;
    high_score = 0;
    generation = 1;
    intervalID = 0;
    playing_loadbird = false;

    let slider = document.getElementById("frameRate");
    frame_rate = slider.value;
    slider.addEventListener("change", function () {
      pause = false;
      frame_rate = slider.value;
      clearInterval(intervalID);
      intervalID = setInterval(draw, 1000 / frame_rate);
    });
  }

  function startgame() {
    myPipes = [];
    let pipe = new Pipes();
    myPipes.push(pipe);
    intervalID = setInterval(draw, 1000 / frame_rate);
  }

  function updateUI() {
    score = document.getElementById("score");
    score.innerHTML = "Score: " + currentBird.distance;

    birdID = document.getElementById("birdID");
    birdID.innerHTML = "Bird: " + (currentID + 1);

    gen = document.getElementById("generation");
    gen.innerHTML = " Generation: " + generation;

    hc = document.getElementById("highscore");
    hc.innerHTML = "Highest Score: " + high_score;
  }

  function draw() {
    draw_background();
    draw_bird();
    draw_pipe();
    bird_action();
    check_colison();
    currentBird.distance++;
    if (currentBird.distance > high_score) {
      high_score = currentBird.distance;
    }
    updateUI();
  }

  function bird_action() {
    let input = create_input();
    let action = currentBird.predict(input);
    if (action == 1) {
      currentBird.jump();
    }
  }

  function create_input() {
    let closestpipe = null;
    let closestdis = Infinity;

    for (let i = 0; i < myPipes.length; i++) {
      let d = myPipes[i].x + setting.pipe_size - currentBird.x;
      if (d < closestdis && d > 0) {
        closestdis = d;
        closestpipe = myPipes[i];
      }
    }

    let i1 =
      (closestpipe.pipe1Len + 60) / setting.screen_h -
      currentBird.y / setting.screen_h;
    let i2 = closestdis / setting.screen_w;
    let i3 = currentBird.vy / 15;
    return [i1, i2, i3];
  }

  function draw_background() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, setting.screen_w, setting.screen_h);
  }

  function draw_bird() {
    ctx.fillStyle = "red";
    ctx.fillRect(
      currentBird.x,
      currentBird.y,
      setting.bird_size,
      setting.bird_size
    );
    currentBird.updateYpos();
  }

  function draw_pipe() {
    ctx.fillStyle = "white";
    for (let i = 0; i < myPipes.length; i++) {
      ctx.fillRect(
        myPipes[i].x,
        myPipes[i].pipe1Y,
        setting.pipe_size,
        myPipes[i].pipe1Len
      );
      ctx.fillRect(
        myPipes[i].x,
        myPipes[i].pipe2Y,
        setting.pipe_size,
        myPipes[i].pipe2Len
      );
      myPipes[i].updatePipesPos();
    }

    addRemovePipe();
  }

  function addRemovePipe() {
    // add pipe;
    if (
      myPipes[myPipes.length - 1].x + setting.pipe_distance <
      setting.screen_w
    ) {
      let pipe = new Pipes();
      myPipes.push(pipe);
    }

    // remove pipe;
    if (myPipes[0].x + setting.pipe_size <= 0) {
      myPipes.shift();
    }
  }

  function check_colison() {
    if (currentBird.y < 0 || currentBird.y >= setting.screen_h) {
      currentBird.alive = false;
      birdDie();
    }

    for (let i = 0; i < myPipes.length; i++) {
      if (
        (currentBird.y < +myPipes[i].pipe1Len ||
          currentBird.y >= myPipes[i].pipe2Y) &&
        (currentBird.x + setting.bird_size > myPipes[i].x &&
          myPipes[i].x + setting.pipe_size > currentBird.x)
      ) {
        currentBird.alive = false;
        birdDie();
      }
    }
  }

  function birdDie() {
    clearInterval(intervalID);
    if (!playing_loadbird) {
      currentID++;
      if (currentID >= pop_size) {
        nextGen();
        currentID = 0;
      }
      currentBird = myBirds["bird" + currentID];
    } else {
      loadbird();
    }
    startgame();
  }

  function nextGen() {
    calculateFitness();
    let { topBirds, topFitness, topDistance, avgDistance } = findTopBird();

    myBirds = {};

    for (let i = 0; i < keep_size; i++) {
      myBirds["bird" + i] = topBirds[i];
      myBirds["bird" + i].resetFitness();
    }

    for (let i = keep_size; i < pop_size; i++) {
      let random1 = getRandomFromProb(topFitness);
      let random2 = getRandomFromProb(topFitness);
      let parent1 = topBirds[random1];
      let parent2 = topBirds[random2];
      let child = Bird.crossover(parent1, parent2, brain_structure);
      child.birdBrain.mutate(0.05);
      myBirds["bird" + i] = child;
    }
    console.log(`Gen ${generation} averange distance: ${avgDistance}`);
    console.log(topDistance);
    generation++;
  }

  function calculateFitness() {
    let sum = 0;
    for (let i = 0; i < pop_size; i++) {
      sum = myBirds["bird" + i].distance;
    }

    for (let i = 0; i < pop_size; i++) {
      myBirds["bird" + i].fitness = myBirds["bird" + i].distance / sum;
    }
  }

  function findTopBird() {
    // make a array of all the bird
    let temp = [];
    for (let i = 0; i < pop_size; i++) {
      temp.push(myBirds["bird" + i]);
    }
    // sort the array with compare function.
    // https://www.w3schools.com/js/js_array_sort.asp
    temp.sort(function (a, b) {
      if (a.fitness > b.fitness) {
        return 1;
      } else if (a.fitness < b.fitness) {
        return -1;
      }
      return 0;
    });
    // reverse the order so the best bird first.
    temp.reverse();

    let topBirds = temp.slice(0, keep_size);
    let topFitness = [];
    let topDistance = [];
    let avgDistance = 0;

    for (let i = 0; i < keep_size; i++) {
      topFitness.push(topBirds[i].fitness);
      topDistance.push(topBirds[i].distance);
      avgDistance += topBirds[i].distance;
    }
    avgDistance = avgDistance / keep_size;

    if (best_Bird.distance < topBirds[0].distance) {
      best_Bird = topBirds[0];
    }

    return { topBirds, topFitness, topDistance, avgDistance };
  }

  function keyPress(e) {
    if (e.keyCode == 32) {
      currentBird.jump();
    } else if (e.keyCode == 27) {
      if (pause) {
        intervalID = setInterval(draw, 1000 / frame_rate);
        pause = false;
      } else {
        clearInterval(intervalID);
        pause = true;
      }
    }
  }

  function loadbird() {
    playing_loadbird = true;
    fetch(
      "https://raw.githubusercontent.com/JimmyDoan1309/Flappy-Bird-with-NeuralEvolution/master/god_bird.json"
    )
      .then(response => response.json())
      .then(data => play_god_bird(data))
      .catch(err => console.log(err));
  }

  function play_god_bird(data) {
    god_bird = new Bird(brain_structure);
    god_bird.birdBrain.w = data.w;
    god_bird.birdBrain.b = data.b;
    currentBird = god_bird;
    currentID = 0;
    if (intervalID != 0) {
      clearInterval(intervalID);
    }
    startgame();
  }

  function trainbird() {
    generation = 1;
    playing_loadbird = false;
    myBirds = {};
    for (let i = 0; i < pop_size; i++) {
      myBirds["bird" + i] = new Bird(brain_structure);
    }
    currentID = 0;
    currentBird = myBirds["bird0"];
    best_Bird = myBirds["bird0"];

    if (intervalID != 0) {
      clearInterval(intervalID);
    }
    high_score = 0;
    startgame();
  }
};

pause = false;

setting = {
  screen_w: 400,
  screen_h: 300,
  bird_size: 20,
  pipe_size: 60,
  pipe_distance: 150
};
