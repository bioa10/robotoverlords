pipe_gap = 120;
pipe_speed = 2;
class Pipes {
  constructor() {
    this.x = 400;
    this.pipe1Y = 0;
    this.pipe1Len = randomPipeLength(20, 160);
    this.pipe2Y = this.pipe1Len + pipe_gap;
    this.pipe2Len = 300 - this.pipe2Y;
  }

  updatePipesPos() {
    this.x -= pipe_speed;
  }
}

function randomPipeLength(min, max) {
  let random = Math.floor(Math.random() * (max - min)) + min;
  return random;
}
