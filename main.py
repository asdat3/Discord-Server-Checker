import psutil, time, json
from discord_webhook import DiscordWebhook, DiscordEmbed
from tcp_latency import measure_latency

def read_config_file():
    global webhook_url
    global server_name
    global state_critical
    global state_warning
    global icon_url_footer

    with open("config.json","r") as f:
        data = json.load(f)

        webhook_url = data["webhook_url"]
        server_name = data["server_name"]
        state_critical = float(data["state_critical"])
        state_warning = float(data["state_warning"])
        icon_url_footer = data["icon_url_footer"]


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
    if float(get_gb(mem.available)) < state_critical:
        status = "critical"
    elif float(get_gb(mem.available)) < state_warning:
        status = "warning"

    if status == old_status:
        pass #no changes
    else:
        try:
            send_memory_warning(mem=mem, swap=swap, status=status)
            try:
                write_everything(mem=mem, swap=swap, status=status)
            except:
                print("ERROR WRITNG NEW STATUS IN FILE")
        except:
            print("ERROR SENDING WEBHOOK!")



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

    embed.set_footer(text=f"Server Watcher | {server_name}", icon_url=icon_url_footer)

    embed.add_embed_field(name="Memory", value=f'{str(get_gb(mem.total))}GB', inline=True)
    embed.add_embed_field(name="Memory Available", value=f'{str(get_gb(mem.available))}GB', inline=True)
    embed.add_embed_field(name="Status", value=status, inline=True)

    embed.add_embed_field(name="Swap", value=f'{str(get_gb(swap.total))}GB', inline=True)
    embed.add_embed_field(name="Swap Free", value=f'{str(get_gb(swap.free))}GB', inline=True)

    #ping (just to add another field to make it look better)
    ping_here_b = measure_latency(host='8.8.8.8')
    ping_here = round(float(ping_here_b[0]),3)
    embed.add_embed_field(name="Ping", value=f'{str(ping_here)}ms', inline=True)

    webhook = DiscordWebhook(url=webhook_url)
    webhook.add_embed(embed)
    response = webhook.execute()


checking_server = True
while checking_server == True:
    read_config_file()
    try:
        check_memory()
        time.sleep(5)
    except:
        checking_server = False