const express = require('express');
const path = require('path');
const app = express();

// Phục vụ thư mục public làm static files
app.use(express.static(path.join(__dirname, 'public')));

// Trả về index.html cho các route còn lại
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
