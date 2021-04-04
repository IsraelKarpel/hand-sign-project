const express = require('express');
const morgan = require ('morgan');
const mongoose = require('mongoose');

// import the model
const Info = require('./models/info');

const app = express();

// connect to mongodb to collection projectDatabase
const dbURI = 'mongodb+srv://hadar24:hadar246@cluster0.4wfka.mongodb.net/projectDatabase?retryWrites=true&w=majority';
mongoose.connect(dbURI , { useNewUrlParser: true , useUnifiedTopology:true})
    .then((result)=>{
        console.log('connected to db');
        // // listen for request
        app.listen(3000);
    }).catch((err)=>{
        console.log(err)
    });

// register view engine
app.set('view engine', 'ejs');
app.use(morgan('tiny'));
app.use(express.urlencoded({extended: true}));
// interaction with database
app.get('/addInfo', (req, res)=>{
    // create an instase of model info
    const info = new Info({
        url: 'https://www.youtube.com/watch?v=cRGrIn2VHTE 11' ,
        language : 'English 12',
        subtitles : 'abbababadhbashhas'
    });

    // save to db
    info.save()
        .then((result)=>{
            res.send(result);
        })
        .catch((err)=>{
            consloe.log(err);
        })
});

// get all info in database
app.get('/allInfo', (req,res)=>{
    // it finds all the info in database
    Info.find()
    .then((result)=>{
        res.send(result)
    })
    .catch((err)=>{
        consloe.log(err);
    });
})


// find single info in database
app.get('/singleInfo',(req,res)=>{
    Info.findById('60696b171477511af0f7f373')
    .then((result)=>{
        res.send(result)
    }).catch((err)=>{
        consloe.log(err)
    });
})

app.get('/', (req,res)=>{
    res.redirect('/info');
    // const info= [
    //     { head1: 'hiii' , body1: 'bodydydyd' },
    //     { head1:'h2h2h2h', body1: 'bvifbdi'}
    // ];
    //res.send('<p> home page </p>');
    // absolute path
    //res.sendFile('./views/index.html', {root: __dirname});
 //   res.render('index', { info});
});

app.get('/info', (req,res)=>{
    Info.find()
    .then((result)=>{
        res.render('index', {title: 'hadari!', info: result })
        })
        .catch((err)=>{
        console.log(err);
    })
})

app.get('/create', (req,res)=>{
    res.render('create');
})

app.post('/', (req,res)=>{
  //  console.log(req.body);
  // create a new instance of info - excatly what we get from 
  const information = new Info(req.body);

  // save to the database
  information.save()
    .then((result)=>{
        //res.redirect('/');
        res.sendFile('./filePose.pose', {root: __dirname});
    })
    .catch((err)=>{
        consloe.log(err);
    })
});
