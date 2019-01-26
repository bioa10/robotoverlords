class Bird {
  constructor(brain_structure) {
    this.x = 90;
    this.y = 150;
    this.vy = 1;
    this.acc = 1;
    this.alive = true;
    this.fitness = 0;
    this.distance = 0;
    this.birdBrain = new Brain(brain_structure);
  }

  jump() {
    this.vy = -10;
  }

  resetFitness() {
    this.alive = true;
    this.fitness = 0;
    this.distance = 0;
  }

  predict(input) {
    let action = this.birdBrain.predict(input);
    return action;
  }
  updateYpos() {
    if (this.alive) {
      this.y += this.vy;
      if (this.vy < 15) {
        this.vy += this.acc;
      }
    }
  }

  static crossover(p1, p2, brain_structure) {
    let new_bird = new Bird(brain_structure);
    new_bird.birdBrain = Brain.crossover(
      p1.birdBrain,
      p2.birdBrain,
      brain_structure
    );

    return new_bird;
  }
}
