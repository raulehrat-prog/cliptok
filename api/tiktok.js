export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Método não permitido" });
  }

  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: "URL obrigatória" });
  }

  try {
    const response = await fetch(`https://tikwm.com/api/?url=${encodeURIComponent(url)}`);
    const data = await response.json();

    if (!data?.data?.play) {
      return res.status(400).json({ error: "Não foi possível baixar" });
    }

    return res.status(200).json({
      video: data.data.play
    });

  } catch (error) {
    return res.status(500).json({ error: "Erro interno" });
  }
}