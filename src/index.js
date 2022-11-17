const Discord = require("discord.js");
const config = require("./config.json");
const { Client, GatewayIntentBits } = require('discord.js');
const {joinVoiceChannel,createAudioPlayer,createAudioResource} = require('@discordjs/voice')
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(args));
const { EmbedBuilder } = require('discord.js');

const client = new Client({ intents: [GatewayIntentBits.Guilds] });
client.login(config.BOT_TOKEN);


client.on("ready", () => {
    console.log(`Logged in as ${client.user.tag}!`)
  })
  
  client.on("message", msg => {
    if (msg.content === "ping") {
      msg.reply("pong");
    }
  })

  client.on('interactionCreate', async interaction => {
    if (!interaction.isChatInputCommand()) return;
  
    const { commandName } = interaction;
  
    if (commandName === 'ping') {
      await interaction.reply('Pong!');
    } else if (commandName === 'server') {
      await interaction.reply('Server name: MC Gaming United\nTotal members: 15');
    } else if (commandName === 'user') {
      await interaction.reply("Your tag:" + interaction.user.tag);
    } else if (commandName === 'meme') {          
                fetch(`https://meme-api.herokuapp.com/gimme/`)
                .then(res => res.json())
                .then(json => {
                    const embed = new Discord.EmbedBuilder()
                     .setAuthor({name: interaction.user.tag})
                      .setImage(json.url)
                       .setFooter({text: "Command requested by: " + interaction.user.tag})
                        .setColor(16777215)
                        interaction.channel.send ({ embeds: [embed] });
                  })              
    } else if (commandName === 'play') {
      const client = new Client({
        shards:"auto",
        intents:[
          intents.FLAGS.Guilds,
          intents.FLAGS.Guild_Voice_States

        ]
      })
      const Channels = ["1030453486757888060","1030222824884944906","194786501089951746"]
      client.on("ready", async () =>{
        for(const channelid in Channels){
          joinChannel(channelid);
          await new Promise(res=> setTimeout(()=>res(2),500))
        }
        function joinChannel(channelid){
        client.channels.fetch(channelid).then(channel=>{
           const VoiceConnection = joinVoiceChannel({
            channelid: channel.id,
            guildid: channel.guild.id,
            adapterCreator: channel.guild.voiceAdapterCreator
           });
           const resource = createAudioResource("https://www.youtube.com/watch?v=jfKfPfyJRdk")
           resource.volume.setVolume(0.2);
           const player = createAudioPlayer()
           VoiceConnection.subscribe(player);
           player.play(resource);
           player.on("idle", () =>{
            try {
              player.stop()
            }catch(e) {console.log(e)}
            try{
              VoiceConnection.destroy()
            } catch(e) {}
            joinChannel(channel.id) 
        }).catch(console.error)
      }) 
      }
    })
    }
});