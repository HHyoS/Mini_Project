const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const {pool} = require('./db');
const multer = require('multer');

//node 내장 모듈
const PORT = 8080;
const path = require('path');

const upload = multer({
    storage : multer.diskStorage({
        //파일 업로드 위치
        destination : (req, file, done) => {
            done(null, "public/")
        },
        filename : (req,file,done)=>{
            console.log(file);

            //확장자 추출
            const ext = path.extname(file.originalname);

            //확장자를 제외한 이름
            const fileNmaeExeptExt = path.basename(file.originalname, ext);

            //원본 파일이름 + 날짜 + 확장자
            //Date.now() 상세 년월일시초
            const saveFilenName = fileNmaeExeptExt+ Date.now() + ext;
            done(null,saveFilenName);
        }
    })
})
const app = express();

//cors 세팅
app.use(cors());

//http log
app.use(morgan('dev'));

//body 데이터 받아오기
app.use(express.json());

//전역폴더 세팅
app.use("/public", express.static("public"));

app.get("/api/menus", async (req,res) => {
    try{
        const data = await pool.query("SELECT * FROM menus");
        console.log(data);
        return res.json(data[0]);
    }
    catch(error){
        console.log(error);

        return res.json({
            success : false,
            message : "전체 메뉴 목록 조회에 실패하였습니다."
        });
    }
})

app.get("/api/menus/:id", async (req,res) => {
    try{
        const data = await pool.query("SELECT * FROM menus WHERE id = ?",[req.params.id]);
        console.log(data[0]);
        return res.json(data[0][0]);
    }
    catch(error){
        console.log(error);
        return res.json({
            success:false,
            message : "메뉴 조회에 실패하였습니다."
        })
    }
})

app.post("/api/menus", upload.single('file'),async (req,res) => {
    try{

        console.log(req.data);
        const data = await pool.query(`
        INSERT INTO menus (name,description,image_src) VALUES (?,?,?)`, [req.body.name,req.body.description, req.file.path]); 
        return res.json({
            success:true,
            message : "메뉴 등록에 성공하였습니다."
        })
    }catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "메뉴 등록에 실패하였습니다."
        })
    }
})


// 메뉴의 이름과 설명 수정
// id를 입력받아 해당 id에 해당하는 name, description 을 수정
app.patch('/api/menus/:id', async (req,res) => {
    try{
        console.log(req.params);

        const data = await pool.query(`UPDATE menus SET name = ?, description =? where id=?`,
        [req.body.name, req.body.description, req.params.id]);
        return res.json({
            success : true,
            message : "메뉴 정보 수정에 성공하였습니다."
        });
    }
    catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "메뉴 정보 수정에 실패하였습니다."
        })
    }
})


// 이미지 수정
// id를 입력받아서 해당 id의 image_src를 업데이트
app.post('/api/menus/:id/image', upload.single('file'), async (req,res) => {
    try{
        // 기존 id로 찾아서 경로를 찾아낸 후 -> 그것에 해당하는 이미지를 삭제
        const data = await pool.query("UPDATE menus SET image_src = ? WHERE ID = ?",
        [req.file.path, req.params.id]);
        console.log(req.params);

    return res.json({
            success : true,
            message : "메뉴 이미지 수정에 성공하였습니다."
        });
    }
    catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "메뉴 이미지 수정에 실패하였습니다."
        })
    }
})

// 메뉴 삭제
// id를 입력받아 특정 아이디를 db에서 삭제하기는 기능
app.delete("/api/menus/:id", async (req,res) => {
    try{
        console.log(req);
        const data = await pool.query(`DELETE FROM menus WHERE id = ?`, [req.params.id]);

        return res.json({
            success:true,
            message : "메뉴 삭제에 성공하였습니다."
        });
    }
    catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "메뉴 삭제에 실패하였습니다."
        })
    }
})

//주문파트 orders

// 전체 주문목록 출력
app.get("/api/orders", async (req,res) => {
    try{
        // LEFT JOIN은 NULL한 값도 가져옴
        // INNER JOIN은 안가져옴
        // a.id라 하는 이유는 a(orders)의 id를 지칭하는지 b(menus)의 id를 지칭하는지 모르기 때문에 사용!
        // 나머지는 왜a,b를 붙이지 않았나? ( 겹치는 ㅐ뇽을 가지고잇지 않기때문에, 고유한 컬럼들은 사용하지않음)
        const data = await pool.query(`
        SELECT a.id,quantity,request_detail, name, description
        FROM orders as a
        INNER JOIN menus as b
        ON a.menus_id = b.id
        ORDER BY a.id desc`);

        return res.json(data[0]);
    }
    catch(error){
        console.log(error);

        return res.json({
            success : false,
            message : "전체 주문 목록 조회에 실패하였습니다."
        })
    }
})

// 특정 주문번호 상세 조회
app.get("/api/orders/:id", async (req,res) => {
    try{
        const data = await pool.query(`
        SELECT a.id,quantity,request_detail, name, description
        FROM orders as a
        INNER JOIN menus as b
        ON a.menus_id = b.id
        WHERE a.id = ?
        ORDER BY a.id desc`,[req.params.id]);

        return res.json(data[0][0]);
    }
    catch(error){
        console.log(error);

        return res.json({
            success : false,
            message : "특정 주문번호 상세 조회에 실패하였습니다."
        })
    }
})


app.post("/api/orders", async (req,res) =>{
    try{
        // quantity ( 수량 )
        // request_detail ( 주문시 요청사항 )
        // menus_id (db에 menus_id 저장)

        const data = await pool.query(`
        INSERT INTO orders (quantity, request_detail, menus_id)
        VALUES (?,?,?)`, [req.body.quantity, req.body.request_detail, req.body.menus_id])
        return res.json({
            success : true,
            message : "주문에 성공하였습니다."
        })
    }
    catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "주문에 실패하였습니다."
        })
    }
})

//주문내역 수정기능
// id를 입력받아서 주문내역 수정
app.patch('/api/orders/:id', async (req,res) => {
    try{
        console.log(req.params);

        const data = await pool.query(`UPDATE orders SET quantity = ?, request_detail = ?, menus_id = ? WHERE id=?`,
        [req.body.quantity, req.body.request_detail, req.body.menus_id, req.params.id]);
        return res.json({
            success : true,
            message : "주문 정보 수정에 성공하였습니다."
        });
    }
    catch(error){
        console.log(error);
        return res.json({
            success : false,
            message : "주문 정보 수정에 실패하였습니다."
        })
    }
})

app.delete('/api/orders/:id', async (req,res) => {
    try{
        console.log(req.params);

        const data = await pool.query(`DELETE FROM orders WHERE id = ?`,[req.params.id]);

        return res.json({
            success : true,
            message : "주문 취소 성공"
        })
    }
    catch(error){
        return res.json({
            success: false,
            message : "주문 취소 실패"
        })
    }
})
app.listen(PORT, () => console.log(`${PORT} 가동중`));