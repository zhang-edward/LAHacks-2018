const express = require('express');
const bodyParser = require('body-parser');
const formidable = require('formidable');
const path = require('path');
const csvFilePath = './uploads/output.csv';
const csv = require('csvtojson');


const app = express();
app.use(express.static(path.join(__dirname, 'build')));

app.get('/ping', function (req, res) {
 return res.send('pong');
});

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

app.post('/', function (req, res){
    var form = new formidable.IncomingForm();

    form.parse(req);

    form.on('fileBegin', function (name, file){
        file.path = __dirname + '/uploads/' + file.name;
    });

    form.on('file', function (name, file){
        console.log('Uploaded ' + file.name);
    });

    res.sendFile(__dirname + '/public/index.html');
});

app.get('/data', function (req, res) {
    var data = { data: [] };
    csv()
        .fromFile(csvFilePath)
        .on('json',(jsonObj)=>{
            // combine csv header row and csv line to a json object
            // jsonObj.a ==> 1 or 4
            data['data'].push(jsonObj);
        })
        .on('done',(error)=>{
            // console.log(data);
            // console.log('end');
            res.send(data);
        });
});

app.listen(process.env.PORT || 8080);