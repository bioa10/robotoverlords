// Upgraded version of Math.random() which return
// value between 0,1. This return value between -1 -> 1
function randomGaussian(min, max) {
  return Math.random() * (max - min) + min;
}

class Matrix {
  constructor(input, output) {
    let matrix = tf.randomNormal([input, output]);
    matrix = Array.from(matrix.dataSync());
    let newMatrix = [];
    for (let i = 0; i < matrix.length; i += output) {
      newMatrix.push(matrix.slice(i, i + output));
    }
    return newMatrix;
  }

  // Static method are called without instantiating their class
  static clone(arr) {
    let matrix = [];
    for (let i = 0; i < arr.length; i++) {
      let row = [];
      for (let j = 0; j < arr[0].length; j++) {
        row.push(arr[i][j]);
      }
      matrix.push(row);
    }
    return matrix;
  }

  static mutation(arr, mutate_rate) {
    let matrix = [];
    for (let i = 0; i < arr.length; i++) {
      let row = [];
      for (let j = 0; j < arr[0].length; j++) {
        if (Math.random() < mutate_rate) {
          row.push(arr[i][j] + randomGaussian(-0.1, 0.1));
        } else {
          row.push(arr[i][j]);
        }
      }
      matrix.push(row);
    }
    return matrix;
  }

  static crossover(arr1, arr2) {
    let row = arr1.length;
    let col = arr1[0].length;
    let matrix = [];
    for (let i = 0; i < row; i++) {
      let row = [];
      for (let j = 0; j < col; j++) {
        let child_value;
        let chance = Math.random();
        if (chance >= 0.5) {
          child_value = arr1[i][j];
        } else {
          child_value = arr2[i][j];
        }
        row.push(child_value);
      }
      matrix.push(row);
    }
    return matrix;
  }
}

function getRandomFromProb(arr) {
  let temp = tf.tensor(arr);
  // tf.multinomial already have softmax build in.
  let random = tf.multinomial(temp, 1).dataSync()[0];
  return random;
}
