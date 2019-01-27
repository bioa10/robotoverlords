
$('document').ready(function(){
    console.log("Hello");

    var empty = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1];
    var myChart = make_graph(empty);

    var canvas = new fabric.Canvas('drawing_sheet');
    canvas.setBackgroundColor('black');
    drawingfunction(canvas);
    function drawingfunction(c){
        console.log("World");
        c.isDrawingMode = true;
        c.freeDrawingBrush.width = 20;
        c.freeDrawingBrush.color = "#FFFFFF";
    }


    $('#clear_button').click(function(){
        canvas.clear();
    });

    $('#predict_button').click(function(){
        // Get the pixel value of the canvas
        var Image_Data = canvas.getContext('2d').getImageData(0,0,280,280);
        make_prediction(Image_Data);
    });

    canvas.clear();

    async function make_prediction(img){
        let image = tf.fromPixels(img,1);
        image = tf.image.resizeBilinear(image,[28,28]);
        image = tf.reshape(image,[1,28,28,1]);
        image = tf.cast(image,'float32');
        image = image.div(tf.scalar(255.0));

        const model = await tf.loadModel('https://raw.githubusercontent.com/JimmyDoan1309/Tensorflow_js_sample/master/model/model.json');

        // tf.tidy help cleaning up memory after every perdiction.
        const p = tf.tidy(() => {
            // Make prediction, return a tensor
            const prediction = model.predict(image);
            // Convert Tensor into array and reuturn
            const output = Array.from(prediction.dataSync());
            return output;
        });
        // [ ...p ]  unrolled the array into a list of number
        // because Math.max take input as (x1,x2,x3,...) not ([x1,x2,x3,...])
        update_graph(p);
    }

    function update_graph(new_data){
        myChart.data.datasets[0].data = new_data;
        myChart.update();
    }

    function make_graph(p){
        var ctx = document.getElementById("chart");
        var myChart = new Chart(ctx, {
        type: 'bar',
        title: {
            display: false
        },
        data: {
            labels: ['0','1','2','3','4','5','6','7','8','9'],
            datasets: [{
                label: "Probability",
                data: p,
                backgroundColor: 'rgba(255, 100, 0,1)'
            }]
        },

        option: {
            title: {
                display: false
            },
            responsive: true,
            maintainAspectRatio: false
        }

        });

        return myChart;
    }
});

