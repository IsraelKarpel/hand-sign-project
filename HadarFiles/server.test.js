const app = require('./server');
//const express = require('express');
const chai = require('chai');
const should = chai.should();
const Axios = require('axios');
var request = require('request');
const supertest = require("supertest");
const helper = require('./utils');
const { debug } = require('request');

// check getpose endpoint 
// execute the get pose function. the function create new row data and saves it in the db .
// after success an object with message 'success' would be returned.

describe('request getpose', async function () {
    this.timeout(10000);
        it('It shouls return an object with the message finished with status 200', async function () {
            const response = await supertest(app)
            .get('/getpose/?path=https%3A%2F%2Fthepaciellogroup.github.io%2FAT-browser-tests%2Fvideo%2Fsubtitles-en.vtt&lang=en.us')
            .expect(200).then(res=> { return res.body;});
            // check the response
            response.should.be.an('Object');
            response.should.have.a.property('message').which.is.a('string').which.equal('success');
        })
    }
);

// check crreateSentences function .
// execute the function on string of 3 rows. compare the number of output.
describe('createSentenses', async function () {
        it('It should return an array with 3 elements', async function () {
            var str = `
00:16.110 --> 00:18.514
No, nothing at all!
            
00:18.514 --> 00:22.669
Really? and at your right? What do you see at your right side Emo?
            
00:22.669 --> 00:26.111
Umm, the same Proog`
            const resArray = helper.createSentenses(str);
       //    chai.expect(Array.isArray(resArray)).toBeTruthy();
            chai.expect(resArray.length).equal(3);
            
        })
    }
);

// takes the word and fetch all the rows that their description includes this word
// compare the number of rows to the expected.
describe('wordFromClient', async function () {
    this.timeout(10000);

    it('Fetch all the data that contains the input word', async function () {
        const response = await supertest(app)
            .get('/wordFromClient?word=close')
            .expect(200).then(res=> { return res.body;});
       chai.expect(response.length).equal(5);
    })
}
);


