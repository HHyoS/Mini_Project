const mysql = require('mysql2/promise');

const pool = mysql.createPool({

    //aws 주소
    host : "43.200.145.225",

    // db 아이디
    user : "hyo",

    // db 비밀번호
    password : "qktk22",

    //db이름
    database : "order_system",
    waitForConnections : true,
    connectionLimit : 10,
    queueLimit : 0
})

module.exports = {pool};
// 객체로 내보내면 객체로 받아온다.
// const db = require('./db/index");
// 활용시 db.pool.query

//module.exports = pool 변수로 내보내면
// const db = require('./db/index');
// db.query