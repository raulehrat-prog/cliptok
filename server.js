const express = require("express");
const { exec } = require("child_process");
const app = express();

app.use(express.json());
app.use("/clips", express.static("clips"));
app.post("/process", (req, res) => {
  const { link, platform } = req.body;

  exec(`python process.py "${link}" "${platform}"`, (err, stdout, stderr) => {
    if (err) return res.json({ error: err.message });
    if (stderr) console.log(stderr);
    res.json({ result: stdout });
  });
});

app.listen(3000, () => {
  console.log("Servidor rodando em http://localhost:3000");
});