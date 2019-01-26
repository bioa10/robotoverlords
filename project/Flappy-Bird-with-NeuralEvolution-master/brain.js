class Brain {
  // array of number of input, hidden, output nodes;
  constructor(arr) {
    this.w = {};
    this.b = {};
    // exclude the input layer;
    this.layer_length = arr.length - 1;
    for (let i = 1; i < arr.length; i++) {
      this.w["w" + i] = new Matrix(arr[i - 1], arr[i]);
      this.b["b" + i] = new Matrix(1, arr[i]);
    }
  }

  // make prediction
  predict(input_value) {
    let a;
    let z;
    let current_w;
    let current_b;
    this.prediction = tf.tidy(() => {
      a = tf.tensor([input_value]);
      for (let i = 1; i < this.layer_length; i++) {
        current_w = tf.tensor(this.w["w" + i]);
        current_b = tf.tensor(this.b["b" + i]);
        z = tf.add(tf.matMul(a, current_w), current_b);
        a = tf.sigmoid(z);
      }
      current_w = tf.tensor(this.w["w" + this.layer_length]);
      current_b = tf.tensor(this.b["b" + this.layer_length]);
      z = tf.add(tf.matMul(a, current_w), current_b);
      // Action = the index of the maximum value;
      let action = tf.squeeze(tf.argMax(z, 1)); // <- axis;
      // dataSync() return value (as array) Synchronously / freeze the DOM.
      // data() return value (as array) Asynchronously
      return action.dataSync()[0];
    });
    return this.prediction;
  }

  // mutate the network alittle bit
  mutate(mutate_rate) {
    for (let i = 1; i < this.layer_length + 1; i++) {
      this.w["w" + i] = Matrix.mutation(this.w["w" + i], mutate_rate);
      this.b["b" + i] = Matrix.mutation(this.b["b" + i], mutate_rate);
    }
  }

  static crossover(p1_NN, p2_NN, brain_structure) {
    let new_brain = new Brain(brain_structure);
    for (let i = 1; i < brain_structure.length; i++) {
      new_brain.w["w" + i] = Matrix.crossover(
        p1_NN.w["w" + i],
        p2_NN.w["w" + i]
      );
      new_brain.b["b" + i] = Matrix.crossover(
        p1_NN.b["b" + i],
        p2_NN.b["b" + i]
      );
    }
    return new_brain;
  }
}
