const express = require("express");
const { exec } = require("child_process");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());
app.use("/clips", express.static("clips"));

// 🔥 ROTA ÚNICA CORRETA
app.post("/process", (req, res) => {
  const { link, platform } = req.body;

  exec(`python process.py "${link}" "${platform}"`, (err, stdout, stderr) => {
    if (err) return res.json({ error: err.message });

    if (stderr) console.log(stderr);

    // 🔥 retorna lista de clips
    const clips = [];
    for (let i = 0; i < 5; i++) {
      clips.push(`/clips/clip_${i}.mp4`);
    }

    res.json({ clips });
  });
});

// 🔥 SERVIDOR
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Servidor rodando na porta " + PORT);
});