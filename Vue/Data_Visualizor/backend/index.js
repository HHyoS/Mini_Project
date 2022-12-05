const express = require("express");

const app = express();
const PORT = 8081;

const cors = require("cors");
app.use(cors());

const morgan = require("morgan");
app.use(morgan("dev"));

app.use(express.json());

const axios = require("axios");
const dotenv = require("dotenv");
const fs = require("fs");
dotenv.config();

app.get("/data", (req, res) => {
  try {
    res.set("Content-Type", "application/json; charset=utf-8");
    const tempFile = fs.createReadStream("uploads/chart.json");
    return tempFile.pipe(res);
  } catch (error) {
    return res.json(error);
  }
});

app.post("/data", async (req, res) => {
  const { startDate, endDate, timeUnit, device, gender, keywordGroups } =
    req.body;
  try {
    const request_body = {
      startDate: startDate,
      endDate: endDate,
      timeUnit: timeUnit,
      device: device === "all" ? "" : device,
      gender: gender === "all" ? "" : gender,
      keywordGroups: keywordGroups,
    };

    const url = "https://openapi.naver.com/v1/datalab/search";
    const headers = {
      "Content-Type": "application/json",
      "X-Naver-Client-Id": process.env.CLIENT_ID,
      "X-Naver-Client-Secret": process.env.CLIENT_SECRET,
    };
    const response = await axios.post(url, request_body, {
      headers: headers,
    });
    fs.writeFile(
      `./uploads/chart.json`,
      JSON.stringify(response.data.results),
      (error) => {
        if (error) {
          throw error;
        }
      }
    );
    return res.json(response.data.results);
  } catch (error) {
    return res.json(error);
  }
});

app.listen(PORT, () => console.log(`this server listening on ${PORT}`));