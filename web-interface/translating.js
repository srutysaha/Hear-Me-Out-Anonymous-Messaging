const fs = require('fs').promises;
const translate = require('@iamtraction/google-translate');

// Function to split text into sentences
function splitIntoSentences(text) {
    // Improved regex to handle sentences better
    return text.match(/[^.!?]+[.!?]*[\s\n]*/g) || [text];
}

async function translateMessage() {
    try {
        // Read the message from the file
        const message = await fs.readFile('message.txt', 'utf8');
        
        // Split the message into sentences
        const sentences = splitIntoSentences(message);

        // Translate each sentence
        const translatedSentences = await Promise.all(
            sentences.map(async (sentence) => {
                const result = await translate(sentence.trim(), { to: 'en' });
                return result.text;
            })
        );

        // Combine the translated sentences
        const translatedMessage = translatedSentences.join(' ');

        // Save the translated message to a file
        await fs.writeFile('translated_message.txt', translatedMessage);
        
        console.log('Translated message saved to translated_message.txt');
    } catch (error) {
        console.error('Error:', error);
    }
}

translateMessage();
