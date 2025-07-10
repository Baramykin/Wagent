const { Client, LocalAuth } = require('whatsapp-web.js');
const fs = require('fs');
const qrcode = require('qrcode-terminal');
const path = require('path');

let counter = 0;

// Функция для транслитерации кириллицы
function transliterate(text) {
    const rus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя';
    const eng = 'abvgdeejzijklmnoprstufhzcss_y_eua';
    
    return text.toLowerCase().split('').map(char => {
        const index = rus.indexOf(char);
        return index >= 0 ? eng[index] : char;
    }).join('');
}

// Создаем директорию для чатов, если её нет

// Получаем текущую дату и время
const now = new Date();

const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const hours = String(now.getHours()).padStart(2, '0');
const minutes = String(now.getMinutes()).padStart(2, '0');

// Формируем строку даты и времени
const formattedDateTime = `${year}-${month}-${day}_${hours}-${minutes}`;


// Очистим файл перед стартом
const baseName = 'chats';
const fileName = `${baseName}_${formattedDateTime}`;

const chatsDir = fileName;
if (!fs.existsSync(chatsDir)) {
    fs.mkdirSync(chatsDir);
}

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox']
    }
});

client.on('qr', qr => {
    console.log('🔐 Отсканируй QR-код:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('✅ Клиент готов.');

    const files = fs.readdirSync('.')
    .filter(f => f.startsWith('contacts_') && f.endsWith('.txt'))
    .sort()
    .reverse();
    console.log('Самый новый файл:', files[0]);
    
    const contactFile = files[0];
    const lines = fs.readFileSync(contactFile, 'utf8')
        .split('\n')
        .filter(Boolean);

    for (const line of lines) {
        const number = line.split(',')[1].trim();
        const chatId = `${number}@c.us`;

        counter++;

        try {
            const chat = await client.getChatById(chatId);
            const messages = await chat.fetchMessages({ limit: 40 }); // 40 сообщений

            console.log(`💬 Получаем сообщения от ${number}...`);
            
            // Получаем имя контакта
            const contact = await chat.getContact();
            const contactName = contact.pushname || contact.name || 'Без_imeni';
            
            // Создаем имя файла с номером и транслитерированным именем
            const safeFileName = `${counter}_${number}_ ${contactName}`;
            const chatFileName = path.join(chatsDir, `${safeFileName}.txt`);
            
            // Формируем содержимое файла
            let chatContent = `Номер: ${number}\n`;
            chatContent += `Имя: ${contactName}\n`;
            chatContent += '='.repeat(50) + '\n\n';

            // Изменяем порядок сообщений - новые сверху
            for (const msg of messages) {
                const sender = msg.fromMe ? 'Вы' : 'Контакт';
                const timestamp = new Date(msg.timestamp * 1000).toLocaleString();
                chatContent += `[${timestamp}] ${sender}: ${msg.body}\n`;
            }

            // Сохраняем чат в файл
            fs.writeFileSync(chatFileName, chatContent, 'utf8');
            console.log(`✅ Чат сохранен в файл: ${chatFileName}`);

        } catch (err) {
            console.error(`❌ Ошибка при получении чата ${number}: ${err.message}`);
        }
    }

    console.log('\n🎉 Обработка завершена.');
    console.log(`📁 Все чаты сохранены в директории: ${chatsDir}`);
    process.exit(0);
});

client.initialize();
