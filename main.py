import psutil, time
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook_url = "https://discord.com/api/webhooks/802329024818053153/FeHP0X74VqDrFY08KUdBAL_6odJB42EVYoXsnHoVYiuPOiFxVJ4lnwWp6A4l7c0WAmMQ"
server_name = "Server1"

def get_gb(bytes_input):
    gb_unrounded = bytes_input / 1073741824
    gb_rounded = round(gb_unrounded,2)
    return(gb_rounded)

def read_old_memory():
    with open("DB/memory/old_avail_mem.txt","r") as f:
        content = f.read()
    return(float(content))

def read_old_swap():
    with open("DB/memory/old_avail_swap.txt","r") as f:
        content = f.read()
    return(float(content))

def read_old_status():
    with open("DB/memory/old_status.txt","r") as f:
        content = f.read()
    return(str(content))

def write_everything(mem, swap, status):
    #print("writing...")
    with open("DB/memory/old_status.txt","w") as f:
        f.write(status)
    with open("DB/memory/old_avail_mem.txt","w") as f:
        f.write(str(mem.available))
    with open("DB/memory/old_avail_swap.txt","w") as f:
        f.write(str(swap.free))


def check_memory():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print("\nmem: " + str(get_gb(mem.total)))
    print("mem free: " + str(get_gb(mem.available)))
    print("swap: " + str(get_gb(swap.total)))
    print("swap free: " + str(get_gb(swap.free)))

    old_available_mem = read_old_memory() #not used anyways
    old_available_swap = read_old_swap() #not used anyways
    old_status = read_old_status()

    status = "good"
    if float(get_gb(mem.available)) < 0.5:
        status = "critical"
    elif float(get_gb(mem.available)) < 1:
        status = "warning"

    if status == old_status:
        pass #no changes
    else:
        try:
            send_memory_warning(mem=mem, swap=swap, status=status)
        except:
            print("ERROR SENDING WEBHOOK!")

    write_everything(mem=mem, swap=swap, status=status)



def send_memory_warning(mem, swap, status):
    if status == "good":
        color_bla = 8311585
    elif status == "warning":
        color_bla = 16312092
    elif status == "critical":
        color_bla = 13632027
    else:
        color_bla = 13632027

    embed = DiscordEmbed(title=f'Memory {status} [{server_name}]', description=f'{server_name} {status}', color=color_bla)

    embed.set_footer(text=f"Server Watcher | {server_name}", icon_url="https://cdn.discordapp.com/attachments/736233445394481242/802330569160654878/drunk.png")

    embed.add_embed_field(name="Memory", value=f'{str(get_gb(mem.total))}GB', inline=True)
    embed.add_embed_field(name="Memory Available", value=f'{str(get_gb(mem.available))}GB', inline=True)

    embed.add_embed_field(name="Status", value=status, inline=True)

    embed.add_embed_field(name="Swap", value=f'{str(get_gb(swap.total))}GB', inline=True)
    embed.add_embed_field(name="Swap Free", value=f'{str(get_gb(swap.free))}GB', inline=True)

    webhook = DiscordWebhook(url=webhook_url)
    webhook.add_embed(embed)
    response = webhook.execute()


checking_server = True
while checking_server == True:
    try:
        check_memory()
        time.sleep(5)
    except:
        checking_server = False