import datetime
import os
import random
import re
import time

from beem import Steem
from beem.account import Account

# =========================================================================
# GITHUB ACTIONS RUNTIME DELAY BUFFER
# =========================================================================
random_delay_seconds = random.randint(60, 600)
print(f"[DELAY] Sleeping {random_delay_seconds / 60:.1f} minutes before running...")
time.sleep(random_delay_seconds)

# =========================================================================
# 1. CONFIGURATION
# =========================================================================
MY_ACCOUNT = "gikunju"
TARGET_COMMUNITIES = [
    "hive-166405"
]
BASE_TAGS = ["history", "stories", "steemexclusive"]
MIN_RC_THRESHOLD = 60.0

STEEM_NODES = [
    "https://api.moecki.online",
    "https://api.campingclub.me",
    "https://api2.justyy.com",
    "https://api3.justyy.com",
    "https://steem-proxy.gikunju.workers.dev",
]

# =========================================================================
# 2. 50 SHORT HISTORICAL STORIES (HEADING, TOPIC TAG, NATURAL STORY)
# =========================================================================
HISTORICAL_STORIES = [
    {
        "heading": "The Lighthouse That Guided Ships by Fire and Mirrors",
        "tag": "alexandria",
        "story": (
            "Off the coast of Alexandria on the island of Pharos, builders stacked pale limestone blocks into a tower that sailors could spot long before the harbor came into view. "
            "At the top, workers kept a roaring fire fed with wood and oil while polished bronze mirrors angled the light across the water. "
            "For centuries it did more than keep ships off the rocks; it turned a tricky stretch of Mediterranean coastline into a busy crossroads where grain, glass, and letters changed hands every day."
        ),
    },
    {
        "heading": "A Clay Tablet Complaint That Outlived Its City",
        "tag": "mesopotamia",
        "story": (
            "Around 1750 BCE in southern Mesopotamia, a customer named Nanni pressed a wedge-shaped stylus into wet clay to complain about a botched copper delivery from a merchant named Ea-nasir. "
            "He argued that the ingots were substandard and that his messenger had been treated poorly on the road. "
            "Thousands of years later, archaeologists dug up the tablet in the ruins of Ur, turning an everyday business dispute into one of the clearest snapshots of ancient trade."
        ),
    },
    {
        "heading": "How Paper Changed Books in Tang China",
        "tag": "china",
        "story": (
            "Before paper became common, readers in China wrestled with heavy bundles of bamboo strips tied together with cord or expensive silk rolls that took ages to prepare. "
            "Using bark, hemp, and old rags beaten into pulp and dried on screens gave scribes a lighter, cheaper surface that folded neatly and traveled easily. "
            "Once paper spread through workshops and offices, records multiplied, exams grew more accessible, and ideas moved faster across regions."
        ),
    },
    {
        "heading": "The Cedar Ships of Byblos",
        "tag": "phoenicia",
        "story": (
            "Along the eastern shore of the Mediterranean, the port of Byblos became famous for shipping tall cedar logs down to Egypt where timber was scarce. "
            "Carpenters prized the wood for its straight grain, strength, and pleasant scent that kept insects away inside temples and royal boats. "
            "Those timber runs helped tie coastal cities into regular sea routes long before long-distance sailing became routine."
        ),
    },
    {
        "heading": "Running Relay Messages Across the Persian Road",
        "tag": "persia",
        "story": (
            "Across the vast stretch of the Achaemenid Empire, packed gravel roads linked satrap capitals from Sardis to Susa with posting stations spaced a day's ride apart. "
            "Fresh horses and riders waited at each stop so urgent dispatches could pass hand to hand without waiting for a single rider to rest. "
            "Herodotus marveled at how fast news moved along the route, comparing the couriers' pace to birds in flight."
        ),
    },
    {
        "heading": "The Water Clocks That Kept Quiet Time in Athens",
        "tag": "greece",
        "story": (
            "In Athenian law courts, speakers did not get to ramble until the magistrate lost patience; a water clock, or clepsydra, measured out their allotted minutes. "
            "Water dripped steadily from a marked vessel through a small opening at the bottom, letting clerks stop the flow when documents were read aloud. "
            "It was a simple trick of gravity and steady flow, yet it brought fairness and order to noisy public arguments."
        ),
    },
    {
        "heading": "Volcanic Ash Freezing a Busy Street in Pompeii",
        "tag": "pompeii",
        "story": (
            "In the late summer of 79 CE, Mount Vesuvius sent up a dark column of ash and pumice that buried the town of Pompeii in less than a day. "
            "Because the hot debris sealed streets, bakeries, and courtyards away from air and rain, everyday details stayed intact beneath the ground. "
            "Walk through the excavated lanes today and you can still see wagon ruts in the paving stones and faded wall notices advertising gladiator bouts."
        ),
    },
    {
        "heading": "The Iron Pillar That Barely Rusts in Delhi",
        "tag": "india",
        "story": (
            "Standing in the Qutb complex in Delhi is a seven-meter iron pillar forged during the Gupta era that has faced monsoon rain and heat for over fifteen centuries. "
            "Instead of flaking away into heavy rust, its surface formed a thin, protective layer of iron hydrogen phosphate aided by phosphorus in the smelting process and slag left in the metal. "
            "Early smiths did not use modern chemistry terms, yet their practical skill produced metal that still surprises visitors."
        ),
    },
    {
        "heading": "Silk, Spices, and Glass Along Desert Trails",
        "tag": "silkroad",
        "story": (
            "No single traveler walked the entire Silk Road in one sitting; goods passed through dozens of hands between Chang'an, Samarkand, and the Mediterranean ports. "
            "Caravans carried woven silk, jade, horses, glassware, and spices across mountain passes and oasis towns where languages mixed in crowded markets. "
            "Even when wars or weather slowed trade, stories, recipes, and craft techniques kept slipping across borders."
        ),
    },
    {
        "heading": "Monks Copying Manuscripts by Candlelight",
        "tag": "medieval",
        "story": (
            "In a quiet scriptorium during the Middle Ages, a scribe spent months bending over scraped calfskin parchment with a trimmed goose quill and oak-gall ink. "
            "One slip of the blade or a smudge of ink could ruin an entire page, so patience mattered just as much as neat lettering. "
            "Thanks to those slow, painstaking hours, works of history, poetry, and theology survived centuries when few copies existed."
        ),
    },
    {
        "heading": "Timbuktu's Libraries in the Sand",
        "tag": "mali",
        "story": (
            "By the fourteenth and fifteenth centuries, Timbuktu had grown into a lively center of learning where scholars copied and collected manuscripts on astronomy, law, medicine, and poetry. "
            "Families kept chests of handwritten pages in courtyard homes, passing books down from one generation to the next. "
            "When trouble threatened the region in later years, locals quietly hid thousands of manuscripts in trunks and cellars to keep them safe."
        ),
    },
    {
        "heading": "A Map Drawn for a Sultan on Gazelle Skin",
        "tag": "cartography",
        "story": (
            "In 1513, Ottoman admiral and mapmaker Piri Reis put together a detailed world chart on gazelle skin using earlier portolan charts and sea accounts. "
            "He drew compass lines radiating across the Atlantic and noted where information came from and where gaps remained. "
            "Though only a fragment of the map survives today, it shows how sailors pieced together fresh ocean news with older charts."
        ),
    },
    {
        "heading": "Movable Metal Type in Mainz",
        "tag": "printing",
        "story": (
            "Around 1450 in Mainz, Johannes Gutenberg combined a durable lead-tin-antimony alloy, an adjustable hand mold for casting crisp type, oil-based ink, and a screw press. "
            "Instead of carving a whole block for a single page, printers could rearrange individual letters for the next sheet and run off dozens of copies quickly. "
            "Books stopped being rare treasures locked in a few collections and started showing up in towns across Europe."
        ),
    },
    {
        "heading": "The Spice Islands That Drew Ships Across Oceans",
        "tag": "spices",
        "story": (
            "Tiny nutmeg and clove trees growing on a handful of volcanic islands in the Maluku archipelago once sparked global voyages and fierce rivalries. "
            "In colder climates, those spices were prized for flavoring food, preserving meat, and trading at huge markups once they reached Europe. "
            "Chasing a handful of fragrant seeds pushed navigators into unfamiliar waters and reshaped trade networks worldwide."
        ),
    },
    {
        "heading": "Stone Terraces Carved Into the Andes",
        "tag": "inca",
        "story": (
            "Farming steep mountain slopes in the Andes meant fighting thin soil, cold nights, and sudden downpours that could wash crops straight down a hillside. "
            "Inca engineers built wide stone-walled terraces filled with layered gravel and rich soil, creating flat steps that held moisture and moderated temperatures. "
            "Paired with careful canal systems, those mountain steps let communities grow potatoes, maize, and quinoa at high altitudes."
        ),
    },
    {
        "heading": "The First Printed Newspaper in Antwerp",
        "tag": "newspapers",
        "story": (
            "Before regular newspapers, people relied on town criers, posted sheets, or handwritten newsletters sent between merchants and diplomats. "
            "In the early seventeenth century, weekly news sheets began appearing on set days, gathering dispatches from different cities onto a single printed page. "
            "Readers could suddenly follow shipping news, wars, and court gossip on a predictable schedule."
        ),
    },
    {
        "heading": "Tulip Bulbs and Wild Prices in Amsterdam",
        "tag": "netherlands",
        "story": (
            "When tulips arrived in the Dutch Republic from the Ottoman world, growers fell in love with their bold colors and streaked petals. "
            "Demand for rare bulbs climbed so fast in the 1630s that traders bought and sold contracts for bulbs still sitting underground waiting for spring. "
            "When confidence suddenly cooled in early 1637, prices tumbled almost overnight, leaving a famous cautionary tale about market hype."
        ),
    },
    {
        "heading": "A Clockmaker's Quest to Solve Longitude",
        "tag": "navigation",
        "story": (
            "At sea, finding how far north or south you were was fairly straightforward with the stars or sun, but finding east or west meant knowing the exact time back home. "
            "Pendulum clocks swung wildly on rolling decks and lost accuracy in shifting temperatures and damp sea air. "
            "Yorkshire carpenter John Harrison spent decades building marine timekeepers that kept steady time at sea, making ocean navigation far safer."
        ),
    },
    {
        "heading": "Coffeehouses as Neighborhood Think Tanks",
        "tag": "coffee",
        "story": (
            "When dark, bitter coffee reached seventeenth-century London, coffeehouses quickly opened their doors for the price of a small cup. "
            "Patrons gathered around long tables to read news sheets, argue politics, talk marine insurance, and test out scientific ideas. "
            "Because a cup cost little and liquor stayed off the menu, people from many walks of life lingered and swapped news for hours."
        ),
    },
    {
        "heading": "Pumping Water Out of Deep Coal Mines",
        "tag": "steam",
        "story": (
            "As miners dug deeper for coal in Britain, groundwater kept flooding the shafts faster than horse-drawn buckets could haul it out. "
            "Early steam engines from Thomas Newcomen and later James Watt used steam and cooling to drive big pumps that kept workings dry. "
            "Cheap coal powered the pumps, and dry mines produced more coal, feeding a cycle that helped drive industrial change."
        ),
    },
    {
        "heading": "The Rosetta Stone's Three Scripts",
        "tag": "egypt",
        "story": (
            "French soldiers rebuilding a fort near Rashid in 1799 uncovered a broken slab of dark stone bearing the same royal decree in three scripts. "
            "Ancient Greek sat at the bottom alongside Egyptian hieroglyphs and demotic script, giving scholars a crucial starting point. "
            "By matching royal names like Ptolemy and Cleopatra across the texts, Jean-Francois Champollion helped crack the reading of hieroglyphs."
        ),
    },
    {
        "heading": "Tapping Out Messages Along Copper Wires",
        "tag": "telegraph",
        "story": (
            "Before the electric telegraph, a message from one city to another could only travel as fast as a horse, a train, or a semaphore arm on a hill. "
            "Sending short and long pulses of electricity down wire let operators spell out words across miles almost instantly. "
            "Suddenly railroad dispatchers could prevent head-on collisions, and newspapers printed news from distant towns the very next day."
        ),
    },
    {
        "heading": "Nightingale's Lanterns in Scutari",
        "tag": "nursing",
        "story": (
            "During the Crimean War in 1854, military hospitals across the Bosphorus at Scutari were overcrowded, filthy, and short on basic supplies. "
            "Florence Nightingale and her team of nurses set to work cleaning wards, organizing linen and food, and keeping careful records of illness and recovery. "
            "Her clear charts and relentless push for sanitation helped turn nursing into a respected profession and reshaped hospital care."
        ),
    },
    {
        "heading": "Laying Cable Beneath the Atlantic",
        "tag": "cables",
        "story": (
            "Linking Europe and North America by undersea telegraph cable took years of trial, broken lines, and heavy ships straining across rough water. "
            "An early cable in 1858 worked for only a few weeks before failing, leaving skeptics convinced the ocean floor was too harsh. "
            "When a stronger cable succeeded in 1866, messages that once took weeks by steamer crossed the ocean in minutes."
        ),
    },
    {
        "heading": "The Great Exhibition's Glass Palace",
        "tag": "london",
        "story": (
            "In 1851, London's Hyde Park hosted a massive glass-and-cast-iron hall built from prefabricated parts in just a few months. "
            "Inside, millions of visitors walked past steam engines, looms, telescopes, furniture, and crafts from dozens of countries. "
            "For many people seeing trains and industrial goods for the first time, the building itself felt like a glimpse into another era."
        ),
    },
    {
        "heading": "From Wet Glass Plates to Pocket Cameras",
        "tag": "photography",
        "story": (
            "Early photographers had to coat heavy glass plates right before taking a shot and develop them before the chemicals dried. "
            "Flexible roll film and simple box cameras changed the habit from a studio chore into something ordinary people could carry on trips. "
            "Family snapshots, street scenes, and travel photos began filling albums in ordinary homes rather than just formal portraits."
        ),
    },
    {
        "heading": "A Bicycle Boom That Changed Street Clothes",
        "tag": "bicycles",
        "story": (
            "Once safety bicycles with equal-sized wheels, chain drives, and air-filled rubber tires arrived in the late nineteenth century, riding became smooth and steady. "
            "Men and women alike rode out to parks and country roads for exercise and independence without waiting for a carriage timetable. "
            "Long, stiff skirts got caught in chains and spokes, helping push practical bloomers and looser outfits into everyday view."
        ),
    },
    {
        "heading": "Wireless Signals Reaching Ships at Sea",
        "tag": "radio",
        "story": (
            "Sending Morse code through the air without wires sounded like magic to sailors who had always relied on flags, flares, or whistles in fog. "
            "Shipboard wireless sets let captains send distress calls and receive weather reports hundreds of miles from land. "
            "Before long, radio waves were carrying voices and music into living rooms, turning a maritime tool into everyday entertainment."
        ),
    },
    {
        "heading": "Twelve Seconds Above Kitty Hawk",
        "tag": "aviation",
        "story": (
            "On a chilly December morning in 1903 on the sandy dunes near Kitty Hawk, Wilbur and Orville Wright took turns testing their motor-driven flyer. "
            "The first powered flight lasted just twelve seconds and covered little more than the wingspan of a modern airliner. "
            "It was brief and bumpy, yet it proved controlled, powered flight was possible and set off decades of rapid design."
        ),
    },
    {
        "heading": "Moldy Petri Dish to Life-Saving Medicine",
        "tag": "penicillin",
        "story": (
            "Returning to his lab in 1928, Alexander Fleming noticed a patch of blue-green mold on a culture dish where nearby bacteria had stopped growing. "
            "That accidental observation pointed to a natural substance that could fight infections that once turned minor cuts into deadly threats. "
            "Years later, chemists and wartime production teams scaled up penicillin so it could reach patients on a wide scale."
        ),
    },
    {
        "heading": "The Library That Saved Ancient Scrolls in a Villa",
        "tag": "herculaneum",
        "story": (
            "Buried beside Pompeii in 79 CE, a seaside villa at Herculaneum held hundreds of rolled papyrus scrolls carbonized by intense volcanic heat. "
            "Because the scrolls looked like brittle black lumps, early attempts to unroll them tore fragile text to pieces. "
            "Modern X-rays and imaging tools have slowly begun reading hidden words inside charred rolls without breaking them apart."
        ),
    },
    {
        "heading": "A Desert Well That Kept Caravans Alive",
        "tag": "caravans",
        "story": (
            "Across dry stretches of North Africa and the Arabian Peninsula, a single hidden well could decide whether a caravan made its next stage safely. "
            "Guides memorized rock shapes, wind-carved dunes, and star positions to hit water holes that looked invisible from a distance. "
            "Around those watering stops, merchants traded salt, gold, dates, and news before packing up before the midday heat."
        ),
    },
    {
        "heading": "Building Bridges Without Mortar in the Andes",
        "tag": "engineering",
        "story": (
            "Inca masons shaped granite and limestone blocks so carefully that stones locked together tightly without mortar to hold them in place. "
            "Slight inward tilts and rounded edges helped walls flex a little during earthquakes instead of cracking straight through. "
            "Many of those stone foundations still stand firm today, outlasting later walls built around them."
        ),
    },
    {
        "heading": "The First Subway Beneath London's Streets",
        "tag": "railways",
        "story": (
            "Horse-drawn omnibuses clogged nineteenth-century streets so badly that moving a few miles across London could take all afternoon. "
            "Opening the Metropolitan Railway in 1863 put passenger trains underground, letting commuters glide past traffic jams beneath the city. "
            "Early steam locomotives pumped smoke into tunnels, making electric traction a welcome relief when underground lines expanded."
        ),
    },
    {
        "heading": "Postage Stamps That Simplified Sending Letters",
        "tag": "postal",
        "story": (
            "Before adhesive postage stamps became standard in 1840, recipients often paid high fees based on distance and page count when a letter arrived. "
            "Putting a small gummed label on the envelope showed postage was already paid and made sorting mail much faster for clerks. "
            "Cheaper, predictable rates encouraged families, workers, and businesses to write letters far more often."
        ),
    },
    {
        "heading": "Glass Blowers of Murano Guarding Their Craft",
        "tag": "venice",
        "story": (
            "On the Venetian island of Murano, glassmakers shaped molten silica with blowpipes, jacks, and shears into clear goblets, mirrors, and colorful beads. "
            "Authorities moved furnaces to the island partly to cut down on city fires and partly to keep skilled techniques close to home. "
            "Even today, the rhythmic turn of a blowpipe and the quick snip of shears look much like workshops centuries ago."
        ),
    },
    {
        "heading": "How Canning Kept Sailors' Meals Safer",
        "tag": "food",
        "story": (
            "Long sea voyages once meant living on salted pork, hardtack biscuits, and dried beans that spoiled easily and left crews short on nutrients. "
            "Sealing food in airtight containers and heating it thoroughly slowed spoilage and gave travelers access to vegetables, stews, and fruit. "
            "First tested for military rations and expeditions, canned food soon made its way onto everyday pantry shelves."
        ),
    },
    {
        "heading": "A Tiny Transistor With a Giant Footprint",
        "tag": "electronics",
        "story": (
            "Bulky, hot vacuum tubes once powered radios and early computers, burning out often and eating up heavy electric current. "
            "In 1947 at Bell Labs, researchers demonstrated a solid-state transistor that could amplify and switch electrical signals in a tiny package. "
            "Shrinking that switching job down to microscopic silicon circuits laid the groundwork for portable radios, phones, and modern computers."
        ),
    },
    {
        "heading": "A Beeping Sphere Circling Earth in 1957",
        "tag": "space",
        "story": (
            "On October 4, 1957, Sputnik 1 entered orbit and sent out steady radio beeps that amateur operators and scientists picked up around the world. "
            "It was a small metal sphere with four antennas, yet its orbit showed that machines could circle the planet above the atmosphere. "
            "Within just over a decade, spaceflight went from a single radio beacon to humans walking on the Moon."
        ),
    },
    {
        "heading": "The Stone Circles of Senegambia",
        "tag": "senegambia",
        "story": (
            "Scattered across parts of Senegal and The Gambia stand hundreds of laterite stone circles and pillars carved centuries ago with striking precision. "
            "Workers quarried the stone, dressed the columns into neat shapes, and arranged them in deliberate rings and lines across open ground. "
            "Archaeological finds around the monuments point to skilled local societies and long-standing burial and ceremonial traditions."
        ),
    },
    {
        "heading": "Ice Harvesting From Frozen Northern Lakes",
        "tag": "ice",
        "story": (
            "Long before electric refrigerators hummed in kitchens, crews in cold northern winters sawed thick blocks of clear ice from frozen ponds and lakes. "
            "Workers stacked the blocks in insulated ice houses packed with sawdust so they would last through warm summer months. "
            "Ships carried cut ice down to warmer ports, cooling drinks, preserving fish, and changing everyday food storage."
        ),
    },
    {
        "heading": "Streetlamps Turning Night Into Strolling Hours",
        "tag": "lighting",
        "story": (
            "Before reliable street lighting, darkness fell hard on towns and cities, keeping most people indoors once the sun went down. "
            "First gas lamps and later electric street lights pushed back the dark along main avenues, bridges, and squares. "
            "Evening markets, theater crowds, and late walks became far more common once streets stayed lit after sunset."
        ),
    },
    {
        "heading": "The Quipu Strings That Tracked Inca Records",
        "tag": "andes",
        "story": (
            "Without a traditional written alphabet, Inca administrators kept detailed records using quipus—cords of cotton or camelid fiber hung from a main line. "
            "Different knot types, positions along a string, and cord colors recorded numbers, categories, and accounts across the empire. "
            "Trained specialists read the knots to track storehouses, tribute, and population tallies across rugged mountain provinces."
        ),
    },
    {
        "heading": "A Quiet Truce Along the Trenches in 1914",
        "tag": "truce",
        "story": (
            "By late December 1914, soldiers on the Western Front had spent months in muddy, cold trenches facing constant danger just yards apart. "
            "On Christmas Eve and Christmas Day in several sectors, singing drifted across no-man's-land and men stepped out to trade small gifts and kick a ball around. "
            "The informal truce faded quickly as orders returned, yet it remains one of the most talked-about pauses of the war."
        ),
    },
    {
        "heading": "Reading Braided Reed Maps in the Marshall Islands",
        "tag": "pacific",
        "story": (
            "Navigating across wide stretches of open Pacific ocean with tiny islands meant reading subtle swells long before land appeared on the horizon. "
            "Marshallese navigators built stick charts from palm ribs and shells to map how ocean swells bent and met around islands. "
            "Apprentices memorized the patterns on land and out at sea, feeling the boat's motion rather than staring at paper."
        ),
    },
    {
        "heading": "The First Cross-Country Drive by Automobile",
        "tag": "roadtrips",
        "story": (
            "In 1903, crossing the United States by car was no smooth highway cruise because paved roads were scarce outside major towns. "
            "Horatio Nelson Jackson, Sewall Crocker, and their dog Bud bumped across dirt ruts, mud, and mountain trails for more than two months. "
            "Flat tires, broken parts, and long detours were part of the trip, proving early cars could survive harsh ground."
        ),
    },
    {
        "heading": "Salt Mines That Preserved Ancient Tools",
        "tag": "mining",
        "story": (
            "Deep inside salt deposits such as those near Hallstatt in Austria, miners chipped away rock salt thousands of years ago using wooden picks and leather packs. "
            "The dry, salty air inside the tunnels kept organic materials from rotting the way they usually do in damp soil. "
            "Archaeologists have found leather shoes, wooden shovels, and wool scraps looking remarkably intact after ages underground."
        ),
    },
    {
        "heading": "The Great Fire That Rebuilt Chicago Taller",
        "tag": "chicago",
        "story": (
            "In October 1871, a fire swept through dry wooden buildings and crowded blocks of Chicago, leaving huge stretches of the city in ruins. "
            "As crews cleared the ashes and rebuilt, architects and builders leaned into fireproof materials, iron and steel framing, and passenger elevators. "
            "Out of the wreckage came a wave of taller commercial buildings that helped shape the modern skyline."
        ),
    },
    {
        "heading": "Carrier Pigeons Carrying Urgent Dispatches",
        "tag": "communications",
        "story": (
            "Homing pigeons have a remarkable knack for finding their way back to their home loft even when carried hundreds of miles away in a basket. "
            "Before field radios were lightweight or dependable everywhere, armies and news agencies strapped tiny messages to birds' legs. "
            "When wires were cut or terrain was rough, a bird flying low overhead often got word through when nothing else could."
        ),
    },
    {
        "heading": "A Small Coin With a Lion and Bull in Lydia",
        "tag": "coinage",
        "story": (
            "In ancient Lydia during the seventh century BCE, metalworkers struck small lumps of electrum—a natural mix of gold and silver—with stamped images. "
            "A government stamp on the metal gave merchants and shoppers a quick way to trust weight and value without weighing bits on a scale every time. "
            "That simple idea caught on fast in nearby trade centers and changed how everyday buying and selling worked."
        ),
    },
]


def sanitize_tag(raw_tag):
    cleaned = re.sub(r"[^a-z0-9-]", "", str(raw_tag).strip().lower())
    return cleaned[:24]


# =========================================================================
# 3. MAIN EXECUTION
# =========================================================================
MY_PRIVATE_POSTING_KEY = os.getenv("STEEM_POSTING_KEY")
if not MY_PRIVATE_POSTING_KEY:
    print("Error: STEEM_POSTING_KEY secret is missing!")
    exit(1)

try:
    stm = Steem(node=STEEM_NODES, keys=[MY_PRIVATE_POSTING_KEY])
    account_info = Account(MY_ACCOUNT, blockchain_instance=stm)
    rc_manabar = account_info.get_rc_manabar()
    current_rc = (rc_manabar["current_mana"] / rc_manabar["max_mana"]) * 100
    print(f"@{MY_ACCOUNT} Resource Credits: {current_rc:.2f}%")

    if current_rc < MIN_RC_THRESHOLD:
        print(f"⚠️ Safety Halt: RC ({current_rc:.2f}%) below {MIN_RC_THRESHOLD}%.")
        exit(0)

    selected_story = random.choice(HISTORICAL_STORIES)
    post_title = selected_story["heading"]
    post_body = f"### {selected_story['heading']}\n\n{selected_story['story']}"
    related_tag = sanitize_tag(selected_story["tag"])

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    raw_slug = "".join(ch if ch.isalnum() or ch.isspace() else "" for ch in post_title.lower())
    slug_part = "-".join(raw_slug.split())[:60]
    post_permlink = f"{slug_part}-{now_utc.strftime('%Y%m%d%H%M')}"

    target_community = random.choice(TARGET_COMMUNITIES)

    final_tags = []
    for t in [target_community, related_tag] + BASE_TAGS:
        clean_t = sanitize_tag(t)
        if clean_t and clean_t not in final_tags:
            final_tags.append(clean_t)

    print(f"Publishing '{post_title}' to {target_community} with tags {final_tags}...")
    stm.post(
        title=post_title,
        body=post_body,
        author=MY_ACCOUNT,
        permlink=post_permlink,
        tags=final_tags,
        parent_author="",
        parent_permlink=target_community,
    )
    print(f"✅ Successfully published to {target_community}!")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    exit(1)
