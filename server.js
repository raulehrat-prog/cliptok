app.post("/process", (req, res) => {
  const { link, platform } = req.body;

  exec(`python process.py "${link}" "${platform}"`, (err, stdout, stderr) => {
    if (err) return res.json({ error: err.message });

    console.log(stdout);

    // 🔥 pega os clips reais do python
    const match = stdout.match(/CLIPS:(.*)/);

    if (!match) return res.json({ clips: [] });

    const clips = match[1]
      .split(",")
      .filter(c => c.trim() !== "");

    res.json({ clips });
  });
});