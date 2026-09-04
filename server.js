const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();

const publicPath = path.join(__dirname, 'public');

// Route kiểm tra phiên bản mã nguồn đang sống trên Render
app.get('/version', (req, res) => {
    res.json({
        status: "LIVE_V3",
        time: new Date().toISOString(),
        public_exists: fs.existsSync(publicPath),
        files_in_public: fs.existsSync(publicPath) ? fs.readdirSync(publicPath) : []
    });
});

// Route phục vụ Avatar ưu tiên
app.get(['/avatar.jpg', '/avatar.png', '/avatar.jpeg', '/Avatar.jpg'], (req, res) => {
    if (fs.existsSync(publicPath)) {
        const files = fs.readdirSync(publicPath);
        const avatar = files.find(f => f.toLowerCase().startsWith('avatar'));
        if (avatar) {
            return res.sendFile(path.join(publicPath, avatar));
        }
    }
    res.status(404).send('Avatar missing in container');
});

app.use(express.static(publicPath));

app.get('*', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on ${PORT}`));
