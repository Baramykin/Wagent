const { Client, LocalAuth } = require('whatsapp-web.js');
const fs = require('fs');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox']
    }
});

//Get Date and Time
const now = new Date();

const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const hours = String(now.getHours()).padStart(2, '0');
const minutes = String(now.getMinutes()).padStart(2, '0');

// Формируем строку даты и времени
const formattedDateTime = `${year}-${month}-${day}_${hours}-${minutes}`;


// Очистим файл перед стартом 
const baseName = 'contacts';
const fileName = `${baseName}_${formattedDateTime}.txt`;

fs.writeFileSync(fileName, '', 'utf8');

// QR код
client.on('qr', (qr) => {
    console.log('📲 Сканируй QR:');
    qrcode.generate(qr, { small: true });
});

// Когда клиент готов
client.on('ready', async () => {
    console.log('✅ Клиент готов! Получаем чаты...');

    const chats = await client.getChats();
    let counter = 0;

    for (const chat of chats) {
        if (!chat.isGroup) {
            const contact = await chat.getContact();
            const name = contact.pushname || contact.name || 'Без имени';
            const number = contact.number;
            counter++;

            const line = `${counter}, ${number}, ${name}\n`;

            fs.appendFileSync(fileName, line, 'utf8');
            console.log(`📱 ${counter}. ${number} | ${name}`);
        }
    }

    console.log(`\n✅ Найдено ${counter} номеров. Все добавлены в contacts.txt`);
    process.exit(0);
});

client.initialize();
