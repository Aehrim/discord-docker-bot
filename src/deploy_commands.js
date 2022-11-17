const { REST, SlashCommandBuilder, Routes } = require('discord.js');
const { clientId, guildId, BOT_TOKEN } = require('./config.json');

const commands = [
	new SlashCommandBuilder().setName('ping').setDescription('Replies with pong!'),
	new SlashCommandBuilder().setName('server').setDescription('Replies with server info!'),
	new SlashCommandBuilder().setName('user').setDescription('Replies with user info!'),
	new SlashCommandBuilder().setName('meme').setDescription('Posts a Random Meme'),
	new SlashCommandBuilder().setName('play').setDescription('Plays the Radio'),
]
	.map(command => command.toJSON());

const rest = new REST({ version: '10' }).setToken(BOT_TOKEN);

rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commands })
	.then((data) => console.log(`Successfully registered ${data.length} application commands.`))
	.catch(console.error);