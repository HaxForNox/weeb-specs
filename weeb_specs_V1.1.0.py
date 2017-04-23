import discord
import asyncio
import time
from fonAPI import FonApi
client = discord.Client()
global programCounter, listMax, programCounter2, searchStatus
searchStatus = False
@client.event
async def on_ready():#prints bot information to show proper login
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    def output(phone):#A neater, cleaner way of formatting the output for the user. When called, will create var requestedPhone and get all the specs and put it in a lovely formatted block.
        requestedPhone = '```Markdown\n'+'#'+phone['DeviceName']+'\n\nWeight: '+phone['weight']+'\n\nDimensions: '+phone['dimensions']+'\n\nSim: '+phone['sim']+'\n\nDisplay: '+phone['type']+' '+phone['size']+'\n\nBattery: '+phone['battery_c']+'\n\nRAM/Storage: '+phone['internal']+'\n\nCPU: '+phone['chipset']+'\n\nRear Camera: '+phone['primary_']+'\n\nFront Camera: '+phone['secondary']+'```'
        return requestedPhone
    def outputFull(phone):#A neater, cleaner way of formatting the output for the user. When called, will create var requestedPhone and get all the specs and put it in a lovely formatted block.
        try:
            IR = phone['infrared_port']
        except:
            IR = 'No'
        try:
            requestedPhone = '```Markdown\n'+'#'+phone['DeviceName']+'\n\nBrand: '+phone['Brand']+'\n\nStatus: '+phone['status']+'\n\nTechnology: '+phone['technology']+'\n\nWeight: '+phone['weight']+'\n\nDimensions: '+phone['dimensions']+'\n\nSim: '+phone['sim']+'\n\nDisplay: '+phone['type']+' '+phone['size']+ ' '+phone['resolution']+'\n\nOS: '+phone['os']+'\n\nBattery: '+phone['battery_c']+'\n\nRAM/Storage: '+phone['internal']+ ' '+phone['card_slot']+'\n\nCPU: '+phone['chipset']+'\n\nGPU: '+phone['gpu']+'\n\nWiFi: '+phone['wlan']+'\n\nIR Blaster: '+IR+'\n\nUSB: '+phone['usb']+'\n\nNetwork: '+phone['_4g_bands']+'\n\nHeadphone jack: '+phone['_3_5mm_jack_']+'\n\nRear Camera: '+phone['primary_']+'\n\nFront Camera: '+phone['secondary']+'```'
        except:
            requestedPhone = '```Markdown\n'+'#'+phone['DeviceName']+'\n\nWeight: '+phone['weight']+'\n\nDimensions: '+phone['dimensions']+'\n\nSim: '+phone['sim']+'\n\nDisplay: '+phone['type']+' '+phone['size']+'\n\nBattery: '+phone['battery_c']+'\n\nRAM/Storage: '+phone['internal']+'\n\nCPU: '+phone['chipset']+'\n\nRear Camera: '+phone['primary_']+'\n\nFront Camera: '+phone['secondary']+'```'
        return requestedPhone

    programCounter =0 #Counts how many times the program has looped. Keep at 0.
    programCounter2=0#Counts how many times the program has looped. Keep at 0.
    listMax = 2 #Do not load more than the set amount of devices, this can be changed to display more in vague searches. Remember python indexes from 0!
    fon = FonApi('24893efe7af58ee35f735a9cda2579659e79fd02213f54ca')#API key
    searchStatus = False #Flag to check if user has made a search or not. Keep at false.
    deviceList = ''
    antiSpam = False

    #querys user for name of the device
    if message.content.startswith('+phone '):
        device=message.content.split('+phone ')[1]
    if message.content.startswith('+Phone '):
        device=message.content.split('+Phone ')[1]
    if message.content.startswith('+PhoneHelp'):
        await client.send_message(message.channel,"""Commands:
+Phone <phone name> (Collects a specsheet if phone found, or returns a list of phones you meant)
+PhoneExact <phone name> (ignores other phone models, searches for your search terms exactly)""")
    if message.content.startswith('+PhoneExact'):
        device=message.content.split('+PhoneExact ')[1]
        phones = fon.getdevice(device)
        #try:
        for phone in phones:
            if str(phone['DeviceName']).lower() == device.lower():
                searchStatus = True
                await client.send_message(message.channel,outputFull(phone))
            else:
                time.sleep(0.7)
                if searchStatus == False:
                    await client.send_message(message.channel,'Device not found')
                searchStatus = True
        #except:
         #   await client.send_message(message.channel,'Device not found, are you sure you typed it properly? :thinking:')
          #  searchStatus = True
#Will be run if searchStatus is False. SearchStatus is only false if +PhoneExact hasn't been run.
    if searchStatus == False:
        try:
            phones = fon.getdevice(device)
        except:
            pass
        try:
            for phone in phones:
                print("1")
                if programCounter > listMax:#Once more than a set amount of variants have been found, it will list the variant names and not the specs. Set max to be listed with listMax
                    searchStatus = True
                    await client.send_message(message.channel,"Search too vague! Here's a list of what I found (Max of 10 results)\nTIP: Use this list, then try +PhoneExact <device name>")
                    for phone in phones:#Reloops to get list of variants
                        print("2")
                        #Output names of variants
                        deviceList = deviceList + phone['DeviceName'] + '\n'
                        programCounter2 = programCounter2 + 1
                        print(phone)
                        #await client.send_message(message.channel,'\nDevice not found.')
                        if programCounter2 > 10:
                            await client.send_message(message.channel,'More devices found, too many to list!')#After 10 variants, it will stop outputting.
                            break
                    await client.send_message(message.channel,'```'+deviceList+'```')
                    break

                programCounter = programCounter + 1#Increment programCounter
            if searchStatus == False:#If there were 3 or fewer variants found, this is run.
                try:
                    for phone in phones:
                        print("3")
                        #Main output is here, if the search was precise enough.
                        await client.send_message(message.channel,output(phone))
                except:
                    pass
            else:
                pass
        #if phone not found in database it will just pass
        except:
            pass
        
client.run('')#bot token used to log in 
