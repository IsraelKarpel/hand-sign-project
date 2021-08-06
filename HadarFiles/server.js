
const express = require('express');
const morgan = require('morgan');
const mongoose = require('mongoose');
const xmlparser = require('express-xml-bodyparser');
var crypto = require('crypto');
const cors = require('cors');
const Path = require('path');
const Axios = require('axios')
const helper = require('./utils');


// import the model
const Info = require('./models/info');
const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cors());
// app.use(express.text())
const fs = require('fs');
// const { url } = require('node:inspector');
var PORT = 4002;
const dbURI = 'mongodb+srv://hadar24:hadar246@cluster0.4wfka.mongodb.net/projectDatabase?retryWrites=true&w=majority';
//const dbURI  = 'mongodb+srv://dbadmin:dbadminpassword@shircluster1.xuxrh.azure.mongodb.net/myFirstDatabase?retryWrites=true&w=majority';
mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then((result) => {
        console.log('connected to db');

        //listen for request
        app.listen(PORT);
    }).catch((err) => {
        console.log(err)
    });


    function hashFunction(path) {
        var hash = crypto.createHash('md5').update(path).digest('hex');
        return hash;
    }
app.get('/', function(req, res) {
    res.status(200).send('Hello world');
});

// app.listen(PORT, function() {
//     console.log('Server is running on PORT:',PORT);
// });


app.get('/wordFromClient', (req, res) => {
    // 1) server return json -> client render dom with js
    Info.find({ 'sentences.text': { $regex: `${req.query.word}`, $options: 'i' } }, (error, data) => {
        if (error) {
            console.log(error);
        } else {
            res.json(data);
        }
    });
});

app.get('/getpose', function (req, res) {
    s = req.body;
    // /getpose/?path=https%3A%2F%2Fthepaciellogroup.github.io%2FAT-browser-tests%2Fvideo%2Fsubtitles-en.vtt&lang=en.us'
    console.log(req.query.path);
    getSubtitlesFromWeb(req.query.path, req.query.lang)
    .then(()=> res.send({message:'success'}))
    .catch( error=> {
        console.log(error);
        res.send({message:'error'})
    });

})


// get subtitles from web and save it in mongodb
function getSubtitlesFromWeb(urlSubtitles, lang) {
    var axios = require('axios');
    var config = {
        method: 'get',
        url: urlSubtitles,
        headers: {}
    };
    return axios(config)
        .then(function (response) {
            // convert subtitles name into hash
            let hashUrl = hashFunction(urlSubtitles);
            console.log(hashUrl);
            const info = new Info({
                hashUrl: hashUrl,
                subtitles: response.data,
                urlPose: urlSubtitles,
                sentences: helper.createSentenses(response.data)
            });
            // save to db
            info.save()
                .then((result) => {
                  getPoseFromPythonServer(urlSubtitles, lang, hashUrl);

                    console.log('saved!');
                    res.send(info);
                });
            // get from server the pose and save it to file system in university
        })
}

async function getPoseFromPythonServer(urlSubtitles, lang, hashPath) {
    const path = require('path');
    const fetch = require('node-fetch');
    console.log('getPoseFromPythonServer');
    const path1 = path.resolve(__dirname, 'posesFromYair', hashPath + '.pose');
    console.log(path1);

    //const res = await fetch('https://nlp.biu.ac.il/~ccohenya8/sign/video/?path=https://thepaciellogroup.github.io/AT-browser-tests/video/subtitles-en.vtt&lang=en.us');
    let url = `https://nlp.biu.ac.il/~ccohenya8/sign/video/?path=${urlSubtitles}&lang=${lang}`;
    const res = await fetch(url);

    const fileStream = fs.createWriteStream(path1);
    await new Promise((resolve, reject) => {
        res.body.pipe(fileStream);
        res.body.on("error", reject);
        fileStream.on("finish", resolve);
    });
}
/*
function createSentenses(str) {
    let result = []
    let timeRegex = /[0-9]{2}:[0-9]{2}\.[0-9]{3} --> [0-9]{2}:[0-9]{2}\.[0-9]{3}/
    let arr = str.split('\n').filter((str, i) => str !== '' && i !== 0)
    arr.forEach(row => {
        if (timeRegex.exec(row)) {
            const [start, end] = row.split(' --> ')
            return result.push({ start: start, end: end, text: '' })
        }
        else result[result.length - 1].text += ` ${row}`
    })
    console.log('result', result);
    return result;
}*/

app.use('/static', express.static('./static'));
app.use('/static', express.static('posesFromYair'));
module.exports = app;
