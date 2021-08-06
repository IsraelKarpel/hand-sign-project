const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Schema - describe the structure of the documents 
// we want to store
const infoSchema = new Schema({
    hashUrl: {
        type: String,
        required : true
    },
    subtitles: {
        type: String,
        required: true
    },
    urlPose: {
        type: String,
        required: true
    },
    sentences: { 
        type: [],
        required: true
    }
}, {timestamps: true });

// create information model
// plurle the Info
const Information = mongoose.model('Info', infoSchema);
module.exports = Information;