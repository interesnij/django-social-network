# -*- coding: utf-8 -*-
from locale import *
import sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

import soundcloud
from music.models import *
from datetime import datetime, date, time


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
page_size = 200
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]

c_rus_list_1 = [
"C-12",
"C-Block",
"C-Bool",
"C-Ro",
"C-Systems",
"C. Jolie",
"C. Tangana",
"C.B.S. (Nikki Jay, 5Плюх, Ykov. Reptar, Frase)",
"C.C. Catch",
"C.C. Peter",
"C.C.Catch",
"C.C.Sexy",
"C.C.TAY",
"C.H.E.W.",
"C.I.C.I feat. Anushka",
"C.J. Chenier",
"C'Sar",
"C2c",
"c7d01",
"Cabante",
"Cabbalero",
"Cabu feat. Love Mansuy",
"Cacciola feat. Vivian B",
"Caceres x Costi",
"Caddi (Константин Берлизов)",
"CADE",
"Cadence",
"Cadmium feat. Grant Dawson & Veronica Bravo",
"Cados & West feat. Carlprit",
"Cady Groves",
"Caeser",
"Cafe Americaine",
"Cafe Del Mar",
"Caffeine",
"Cage The Elephant",
"Caggie",
"Cagri Guzet",
"Cahill",
"Caiaffa feat. MBZ Project",
"Cailin Russo",
"Caiman",
"Caio Monteiro",
"Cairo Son",
"Caiti Baker",
"Caitlyn",
"Caitlyn Cope",
"Caitlyn feat. Bel Mondo",
"Caitlyn feat. Mr. Diliman",
"Caitlyn Scarlett",
"Caius feat. Neigh",]

c_rus_list_2 = [
"Caj Flow",
"Caj Morgan",
"Cajjmere Wray feat. Andrea Godin",
"Cajun",
"Cake",
"Cal Scruby feat. Chris Brown",
"Calabro Project feat. Lady Chica & Helena",
"Calderone Inc.",
"Calectro feat. Anthony Paris",
"Caleidescope feat. Nik Felice",
"Cali",
"Cali Y El Dandee",
"Caliban",
"Calibre",
"California Sun",
"Calippo",
"Call Me Anything",
"Call Me Loop",
"Call Me Steve feat. Eva Bristol",
"Call Of Beat",
"Callabria",
"Callaway & Rosta feat. Marylin",
"Callaway feat. Rosta",
"Called Meyer feat. Kinnie Lane",
"Callibry",
"Callie Reiff",
"Callum Beattie",
"Cally Rhodes",
"Calmani & Grey",
"Calogero",
"Calum Scott",
"Calum Scott & Leona Lewis",
"Calumny",
"Calvin Harris",
"Calvin Logue",
"Calvin O'Commor",
"Calvin West",
"Calvo",
"Calyx & TeeBee",
"Calyx & TeeBee",
"Cam'ron",
"Camay",
"Camden Cox",
"Camela feat. Juan Magan",
"Camelia Crisan",
"Camelot Feat Morgane",
"CamelPhat",
"Cameron Cartio",
"Cameron Ernst",
"Cami & Max Oazo",]

c_rus_list_3 = [
"Cami Hedlinger",
"Cami L",
"Camiel",
"Camikaze feat. Zoe A’dore",
"Camila Cabello",
"Camila feat. Ricky Martin",
"Camilla Brinck",
"Camille Bertault",
"Camille Jones",
"Camille Lou",
"Camilo",
"Caminita feat. Jan Peter",
"Camio",
"Camisra",
"Cammora",
"Camo & Krooked",
"Camoflauge Monk",
"CamoM1Le",
"Camouflage",
"Camp Lo",
"Campsite Dream",
"Can Bonomo",
"Can Demir & Eddy Wata",
"Can-Linn feat. Kasey Smith",
"Canard",
"Canary",
"Canberra & Astrid Suryanto",
"Candi Lynn",
"Candice Boyd feat. French Montana",
"Candice Glover",
"Candice Pillay feat. Kelly Rowland",
"Candy Claws",
"Candy Dufler",
"Candy Dulfer",
"Candy Dulfer and Dave Stewart",
"Candy Shop",
"Candyland",
"Canens Leap",
"Caner Kizil",
"Canned Heat",
"Canon in D Major",
"Cansis vs. Spaceship",
"Cantaffa",
"Cantana Fox",
"Canthina Band",
"Cantoreggi",
"Cap 1 feat. 2 Chainz, Jeremih & Verse Simmonds",
"Capa & Clara Sofie",
"Capa feat. Eric Lumiere",
"Capablanca, La Mverte",]

c_rus_list_4 = [
"Capaletti",
"Capcha One",
"Cape Cub",
"Capercaillie",
"Capital Bra",
"Capital Cities",
"Capital Kings",
"Capitan Jack",
"Capozio",
"CAPPA",
"Cappella",
"Cappuccino",
"Capri",
"Captain Basscut",
"Captain Cuts",
"Captain Hollywood",
"Captain Hooks",
"Captain Ivory",
"Captain Jack",
"Captain Kidd",
"Captain Tajik",
"Capulets",
"Cara Hammond",
"Cara Lee",
"Caravella",
"Carbage",
"Carbon Based Lifeforms",
"Carcer City",
"Carda feat. Adrianna",
"Carda feat. Cirillo",
"Cardi B",
"Cardigans",
"Cardin feat. Denisse Lara",
"Cardinal feat. Arielle Maren",
"Cardinal Zen",
"Cardinale",
"Cardio Beat",
"Carey & Lurrie Bell",
"Carey Bell",
"Caribean Touch",
"Caribou",
"Carina Dahl",
"Carina Ray",
"Carino Cat",
"Carishma feat. Timbaland",
"Carissa Vales",
"Carl Andersson",
"Carl Armstrong",
"Carl Bryan",
"Carl Chapal feat. Paula Lobos",]

c_rus_list_5 = [
"Carl Cox & Nicole Moudaber",
"Carl Daylim",
"Carl De La Croix",
"Carl Douglas",
"Carl Espen",
"Carl Hanaghan & Ted Nilsson feat. Sophie Paul & Kristian Booth",
"Carl Kennedy",
"Carl Louis & Martin Danielle",
"Carl Nicholson",
"Carl Nunes",
"Carl Thomas feat. Snoop Dogg",
"Carl Verheyen",
"Carl Verheyen BAnd",
"Carla Prata",
"Carla's Dreams",
"Carleen & The Groovers",
"Carlie Hanson",
"Carlingford Loch",
"Carlo Del Negro feat. Natalia Damini & Snoop Dogg",
"Carlo Lio",
"Carlo M",
"Carlos Armon",
"Carlos Barbosa",
"Carlos Baute feat. Farina",
"Carlos Estevez",
"Carlos Gallardo feat. Nalaya",
"Carlos Jean",
"Carlos Libedinsky",
"Carlos Lyra",
"Carlos M",
"Carlos Montoya",
"Carlos Navarro",
"Carlos Right",
"Carlos Rivera",
"Carlos Rus & Di Martino feat. Dastone",
"Carlos Russo & Jack Like feat. Jay Jacob",
"Carlos Sadness",
"Carlos Santana",
"Carlos Vara",
"Carlos Vives",
"Carlprit",
"Carlton Alphonso",
"Carly Comando",
"Carly Rae Jepsen",
"Carly Van Skaik",
"Carmen Calin",
"Carmen Electra feat. Bill Hamel",
"Carmen Grace",
"Carmen Linares",
"Carmen Rosa",]

c_rus_list_6 = [
"Carmen Twillie",
"Carmixer",
"Carmody",
"Carmon & Stepz",
"Carnage",
"Carnal feat. Cheka",
"Caro Emerald",
"Carol Anthony aka Havana ft. French Kiss",
"Carol Mae",
"Carol Mag feat. Kevin Ettienne",
"Carol Maraj",
"Carolina Marquez",
"Caroline & Diazz",
"Caroline Brooks",
"Caroline County",
"Caroline Damore feat. Natalie La Rose",
"Caroline Hoier",
"Caroline Koch",
"Caroline Kole",
"Caroline Pennell",
"Caroline Roste",
"Carolyn Gaines",
"Carolyna Blu feat. Donell Lewis",
"Carpark North feat. Nik Og Jay",
"Carpenters",
"Carrie Underwood",
"Carrillo",
"Cars & Calories",
"Carson Taylor",
"Carta & Ares Carter",
"Carta & Mayra",
"Cartacci",
"Carte Blanche feat. Alexis Taylor",
"Carte Blanche feat. Kid Sister",
"CARTEL",
"Cartel Hall",
"Carter Burwell",
"Cartie feat. Kevin McCall",
"Cartoon",
"Caruso & Valenziano feat. S. Afriyie",
"Cary Brothers",
"Cary Kanno",
"Casarano",
"Casaris feat. Morano",
"Casate Conmigo feat. Nicky Jam",
"Casbah feat. Trice",
"Cascada",
"Cascade",
"Case & Pointf",
"Casely",]

c_rus_list_7 = [
"Casey Veggies",
"Cash & Fanizza",
"Cash & Love",
"Cash And Maverick",
"Cash Cash",
"Cash Out feat. Snoop Dogg",
"Cash'U",
"Cashmere Cat",
"CashU",
"Casp feat. ChipaChip",
"Casper Cole feat. Elderbrook",
"Casper Magico & Nio Garcia feat. Jennifer Lopez, Cosculluela, Wisin & Yandel",
"CASPR feat. Lovespeake",
"Cassadee Pope",
"Cassandra Steen",
"Cassandra Wilson",
"Cassey Doreen",
"Cassian",
"Cassiano feat. Cascada",
"Cassie",
"",
"Cassie Steele",
"Cassie Taylor",
"Cassimm feat. Lolly Campbell",
"Cassius & JAW feat. Ryan Tedder",
"Cassius feat. Cat Power & Pharrell Williams",
"Cassius feat. Ryan Tedder",
"Cast",
"Cast Of Galavant feat. Kylie Minogue",
"Castaways",
"Castellina-Pasi",
"Casting Crowns",
"Castion & Jasted",
"Castion x Jack & James",
"Castle feat. Moeazy",
"Castlebed",
"Castly",
"Casual",
"Cat Dealers",
"Cat Delphi",
"Cat Power",
"Cat Power & Coldplay",
"Cat Stevens",
"Cat Torres",
"Catali",
"Catalin Josan",
"Catalina",
"Catalu",
"Catfight",
"Catfish And The Bottlemen",]

c_rus_list_8 = [
"Catfish John Tisdell",
"Catharsis",
"Catherine Russell",
"Cathy Burton",
"Catrina",
"Catrine",
"Cats Love Dogs",
"Catwork Remix Engineers",
"Cautious Clay",
"Cavaro feat. Dominique",
"Cayenna",
"Caymen",
"Cayol",
"Cazoo feat. Emma Addo",
"Cazwell",
"Cazzanova",
"Cazzette",
"Cazzi Opeia",
"Cazztek & Damien N-Drix",
"Cazztek feat. Kiyoshi",
"Cb Milton",
"CbasSlazr",
"CDM Project",
"Ce'Cile feat. Flo Rida",
"Ceasar Kane",
"CeCe",
"Cecilia Dale",
"Cecilia Gayle & DJ Sanny J",
"Cecilie Noer",
"Cecily",
"Cederquist",
"Cedric Gervais",
"Cedrik Zimmermann",
"Cee-Lo Green",
"CeeLo Green",
"Celani & No.Vision feat. Maria",
"Celebrity",
"Celestal feat. Rachel Pearl",
"Celeste",
"Celeste Buckingham",
"Celeste feat. Gotts Street Park",
"Celestial",
"Celia",
"Celie",
"Celine Dion",
"Celldweller",
"Celtic Land",
"Cem Egemen & Quentro",
"Centr",
"Centric",]

c_rus_list_9 = [
"Ceramick Beats feat. Franck Beta",
"Cerf, Mitiska & Jaren",
"Cerritus Ballare",
"Cerrone",
"Certainly Strange feat. Jayydee",
"Cesar Sampson",
"Cesc Lee",
"Ceza",
"Cezar",
"Cezara",
"Cfo",
"Chabud",
"Chacal & Akon",
"Chace & Yellow Claw",
"Chacha",
"Chachi",
"Chachi Paige",
"Chachi feat. Natascha Bessez",
"Chad Cooper & Robaer feat. Emelie Cyreus",
"Chad Lawson",
"Chadash Cort",
"Chael",
"Chagunava",
"Chair Warriors",
"Chaisley Lussier",
"Chaka Khan",
"Chamber 3",
"Chambre 11",
"Chameleon At Night",
"Chamillionaire",
"Champagne Drip",
"Champagne Morning",
"Champian Fulton",
"Champs",
"Chance The Rapper",
"Chanee",
"Chanee & N'Evergreen",
"Chanel West Coast",
"Chanelle Ray",
"Change feat. Nathan Brumley",
"Changing Faces",
"Chango Loco feat. Evee-G",
"Chanmina",
"Chano!",
"Chantel Jeffries",
"Chaos Before Gea",
"Chappo",
"ChapterV",
"Chardy, Kronic, Uberjak'd feat. Leftside",
"Charice",]

c_rus_list_10 = [
"Chariots Of Fire",
"Charisse Mills feat. French Montana",
"Charity Strike",
"Charla K",
"Charlee Remitz",
"Charlene Soraia",
"Charles & Eddie",
"Charles Aznavour",
"Charles B & VCTRY",
"Charles Bradley",
"Charles Brown",
"Charles Fauna",
"Charles Fenckler",
"Charles Kelley feat. Dierks Bentley & Eric Paslay",
"Charles Monroe",
"Charles Perry",
"Charles Reed",
"Charles Simmons",
"Charles Trenet",
"Charles Wright & The Watts 103rd Street Rhythm Band",
"Charleston Clubbers",
"Charley Danone ft. Tony Costa",
"Charli XCX",
"Charlie Ace & The Aquarians",
"Charlie Atom & Michael Fall feat. Joe Bateman",
"Charlie Beale",
"Charlie Cat",
"Charlie Charles feat. Sfera Ebbasta & Mahmood & Fabri Fibra",
"Charlie Clouser",
"Charlie Cunningham",
"Charlie Darker",
"Charlie Dee",
"Charlie G",
"Charlie Hedges feat. Sonny Reeves",
"Charlie Hunter. Norah Jones",
"Charlie Lane",
"Charlie Mauthe vs Joe Hill",
"Charlie Musselwhite",
"Charlie Puth",
"Charlie Rich",
"Charlie Ventura",
"Charlie Ward feat. Flo Rida",
"Charlie Who? feat. Moa Lisa",
"Charlie Wilson",
"Charlie Winston",
"Charlotte",
"Charlotte Black",
"Charlotte Cardin",
"Charlotte Church",
"Charlotte Devaney",]

c_rus_list_11 = [
"Charlotte Gainsbourg",
"Charlotte Lawrence",
"Charlotte OC",
"Charlotte Qvale",
"Charly Black",
"Charly Danone feat. Ella M",
"Charly Lownoise & Mental Theo",
"Charly Mclion",
"Charly Rodriguez",
"Charly'n Black",
"Charmani feat. Flo Rida",
"Charmed",
"Charmes",
"Charming Horses",
"Chart Houz",
"Charusha feat. Nikita Kamensky",
"Chase & Status",
"Chase Atlantic",
"Chasing Abbey",
"Chassio",
"Chawki",
"Chayanne feat. Ozuna",
"Chazz (Of Kiyene)",
"Che Crozz & Orbis",
"Che Jose feat. Sharon Muscat",
"Che'Nelle",
"Cheap Sunglasses",
"Cheat Codes",
"Cheb Miaou feat. Kye Sones",
"Checkmate",
"Chee Karisma",
"Cheeky Girls",
"Cheesa feat. Wafeek",
"CheKa",
"Chekarino Project",
"Chelsea Collins",
"Chelsea Cutler",
"Chelsea Effect",
"Chelsea Grin",
"Chelsea Jade",
"Chelsea Korka",
"Chelsea Lankes",
"Chelsea Wolfe",
"Chemerisoff",
"Chemical Brothers",
"Chenoa",
"Chequerboard",
"Cher",
"Cher Lloyd",
"Cherlise",]

c_rus_list_12 = [
"Chernika",
"Cherry Coke",
"Cherry Laine",
"Cherry Line",
"Cherso",
"Cheryl Ann Fulton",
"Cheryl Cole",
"Chess & Fynn feat. Chad Kowal",
"Chester Page",
"Chester Young",
"Chet Atkins",
"Chet Baker",
"Chet Faker",
"Chevelle",
"Chevy Woodsa",
"Chew Lips",
"Chewy Martins",
"Cheyenne Giles",
"Chezara",
"Chi Chi",
"Chi Ching Ching feat. Sean Paul",
"Chi Pu",
"Chi-Lites",
"ChianoSky",
"Chiara",
"Chic",
"Chicago",
"Chicane",
"Chicco Secci & Benny Benassi feat. Bonnie Calean",
"Chicco Secci & Fabio B",
"Chick Flick",
"Chico & Tom feat. Lee",
"Chico and Tom feat. Lee",
"Chico Rose & Afrojack",
"Chicos De La Fiesta",
"Chiddy Bang",
"Chief Keef",
"Chiko Papoyan",
"Childish Gambino",
"Children Of Freedom feat. Sheylley June",
"Childrens Unite Inc.",
"ChildsPlay",
"Chillbirds",
"Chilli",
"Chilling Matenda",
"Chillo",
"Chillwalker",
"Chilly",
"Chime",
"Chimera State feat. Verenice Buerling",]

c_rus_list_13 = [
"Chimney Records feat. Sean Paul",
"Chimo Bayo",
"Chinah",
"Chinar",
"Chinar Isoyan",
"Chinensis",
"Chingis Lee",
"Chingiz",
"Chino",
"Chinx",
"Chip & Chap",
"Chip Vandiver",
"ChipaChip",
"Chipmunk feat. Keri Hilson",
"Chipmunk feat. Trey Songz",
"Chipper & Estela Martin",
"Chisanity feat. Trey Songz & Dave East",
"Chitto & MAD",
"Chloe & Halle",
"Chloe Black",
"Chloe Gisele",
"Chloe Howl",
"Choc Choc Zoo & Inusa Dawuda",
"Choco feat. Nevve",
"Chocola",
"Chocolate",
"Chocolate Puma",
"ChocQuibTown feat. Becky G",
"Chooze",
"Chopper",
"Chopsy",
"Chorale",
"Chordettes",
"Chordless Theory",
"Chosen Jacobs",
"Chris Agnelli",
"Chris Alder",
"Chris Anderson",
"Chris Arna",
"Chris Arnott, Bass Kleph & BKCA",
"Chris Avantgarde",
"Chris Baco & Meludo",
"Chris Batson",
"Chris Botti",
"Chris Brown",
"Chris Bullen",
"Chris Burton",
"Chris Burton Jacome",
"Chris Cain",
"Chris Carmack",]

c_rus_list_14 = [
"Chris Cockerill & Phil-Lee",
"Chris Cooke",
"Chris Copper & Danny Cadeau",
"Chris Cornell",
"Chris Cortez",
"Chris Crocker",
"Chris Daren",
"Chris Daughtry",
"Chris Dave",
"Chris De Burg",
"Chris De Burgh",
"Chris Decay & Re-lay",
"Chris Decay feat. Ella",
"Chris Doran",
"Chris Duarte",
"Chris Excess",
"Chris Forward & Mace V feat. Eva Kade",
"Chris Galmon & Andy Ztoned",
"Chris Garcia",
"Chris Godber",
"Chris Gold",
"Chris Gomez feat. Danny Miles",
"Chris Grabiec feat. Christina Nicola",
"Chris Hampshire & Thomas Datt",
"Chris Holloway",
"Chris Holsten",
"Chris Hype",
"Chris Isaak",
"Chris J",
"Chris Jacob",
"Chris James",
"Chris James feat. Pusha T",
"Chris Jane",
"Chris Janitor feat. Emma",
"Chris Jones & Steve Baker",
"Chris Jordash feat. JuL & T.M.E.",
"Chris K",
"Chris K & No Antidote feat. Mr. Sax",
"Chris Kaeser",
"Chris Kaye feat. Sean Declase",
"Chris Kool",
"Chris Lain",
"Chris Lake",
"Chris Largo",
"Chris Leao, Allexis & Grace Grey",
"Chris Liebing & Charlotte De Witte",
"Chris Loco feat. Raye",
"Chris Lorenzo feat. Puppah Nas-T & Denise",
"Chris Mack",
"Chris Malinchak",]

c_rus_list_15 = [
"Chris Mann",
"Chris Mayer",
"Chris Memo & Slayback",
"Chris Metcalfe",
"Chris Nasty feat. Ners",
"Chris Night",
"Chris Norman",
"Chris Norton",
"Chris Odd & Moreno Chembele",
"Chris Oliver",
"Chris Olsson",
"Chris Parker",
"Chris Ramos feat. Juvon Taylor",
"Chris Rea",
"Chris Reece",
"Chris Rene",
"Chris Richardson",
"Chris Robinson Brotherhood",
"Chris Rockford & Phil Dinner",
"Chris Rockford feat. Phil Dinner, Simon Fava",
"Chris Salvatore feat. Alius",
"Chris Santana feat. Lady Ana Aya",
"Chris Schweizer",
"Chris SX",
"Chris T Feat. Pat Davis",
"Chris Tall feat. Maydar",
"Chris Tamayo feat. D Note The Beatllionare",
"Chris Team",
"Chris Thompson",
"Chris Thrace",
"Chris Tomlin",
"Chris Torino",
"Chris Trousdale & Nevermind",
"Chris Van Dutch feat. Inverno",
"Chris Victory",
"Chris Viviano",
"Chris Wallace",
"Chris Webby",
"Chris White",
"Chris Willis",
"Chris Wittig",
"Chris Yank",
"Chrisette Michele",
"Chrishan",
"Chriss Palmer feat. BlackSwan",
"Chriss Reiser & Marcus Lanzer",
"Chriss-T",
"Chrissy Depauw",
"Christ Malvin & Ivan Sandhas",
"Christ Ruest & Gene Taylor",]

c_rus_list_16 = [
"Christa Vi",
"Christabelle",
"Christian Amby",
"Christian Bautista & Jessica Sanchez",
"Christian Burns",
"Christian Chavez feat. Anahi",
"Christian Cheval & Gio Di Leva",
"Christian Colier",
"Christian D",
"Christian Di Pasquale",
"Christian Eberhard & Dmitrii Praga feat. Caitlyn",
"Christian French",
"Christian Green",
"Christian Hard",
"Christian Kane",
"Christian Lalama",
"Christian Maxim, Fhazee",
"Christian McBride Trio",
"Christian Nodal & Sebastian Yatra",
"Christian Oscarsson",
"Christian Paul",
"Christian Ramirez feat. Iamdl",
"Christian Rich feat. Jay Sean",
"Christian Rivera",
"Christian Stalker & Kamil Brandt",
"Christian Staymaer",
"Christian Strobe",
"Christian Tanz",
"Christian Vlad",
"Christie & Dream Beats",
"Christie Lamb",
"Christina Aguilera",
"Christina Grimmie",
"Christina Matsa",
"Christina Metaxa",
"Christina Milan",
"Christina Miliane",
"Christina Milian feat. Snoop Dogg",
"Christina Novelli",
"Christina Perri",
"Christina Walls",
"Christine & The Queens feat. Tunji Ige",
"Christine Attacks",
"Christine feat. T La Rock",
"Christine Guldbrandsen",
"Christine Parri",
"Christophe Goze",
"Christophe Mae",
"Christophe Willem",
"Christopher",]

c_rus_list_17 = [
"Christopher Francis & Tony Tweaker",
"Christopher G",
"Christopher Hermann",
"Christopher Lewis",
"Christopher Martin",
"Christopher S",
"Christopher Taylor",
"Christos Fourkis",
"Christos Mastoras",
"Christos Mylordos",
"ChriStylez",
"ChriZ feat. Danielle Senior",
"Chrizzo & Maxim feat. Amanda Wilson",
"Chromak feat. Emily Marques",
"Chromatics",
"Chromeo",
"Chronic",
"Chrystina Sayers",
"Chubby Checker",
"Chucho Valdes",
"Chuck & Norris feat. E-Rockaz",
"Chuck Berry",
"Chuck Colombo",
"Chuck Loeb",
"Chuck Ragan",
"Chuckie",
"Chuga",
"Chung Ha",
"Chunk",
"Chunks & INH feat. Raiide",
"Chunks feat. Rohan Smith",
"Chupa Jane",
"Church & AP",
"Chus & Ceballos",
"Chus Liberata & Jake",
"Chvrches",
"Chynna Phillips",
"Chyno Miranda",
"Chyp-Notic feat. Christina",
"Ciacy",
"Ciako feat. Katia",
"Ciara",
"CiaraCode",
"Ciaran Lavery",
"Ciaran Mcauley",
"Ciaran McAuley & Clare Stagg",
"Ciava",
"Cicada feat. Holly Miranda",
"CID",
"Cidida X Eibol",]

c_rus_list_18 = [
"Cielle",
"Cierra Ramirez",
"Cigarettes After Sex",
"Ciland",
"Cilia",
"Cimo Frankel",
"Cinderella",
"Cindy Alma",
"Cinemascope",
"Cinematic",
"Ciprian Robu",
"Cir.Cuz",
"Cira",
"Circa Waves",
"Cirez D",
"Ciro",
"Cisilia",
"Citizen Cope",
"Citizen Four",
"Citrus Jam",
"City And Colour",
"City Angels feat. Michelle Luttenberger",
"City Girls",
"City Lies",
"City Of Industry",
"City Of Lights",
"City Of Lights feat. Adler",
"City Of The Sun",
"City Rhythm Orchestra",
"Citybois",
"Cityflash",
"Cityzen",
"Cj Ako & Inna",
"Cj RcM",
"CJ Stone",
"Cjw",
"CKKE & Krait",
"CL feat. Diplo, RiFF RaFF & OG Maco",
"CL feat. Will.i.Am",
"Claes Rosen",
"Claes Rosen & Natalie Peris",
"Claes-Goran Fagerstedt",
"Claim Cracker & Eric Chase",
"Claire Guerreso",
"Claire Guerreso & Deepend",
"Claire Laffut & Yseult",
"Claire Willis & Mike Lockin & Mart De Schmidt",
"Clairity",
"Clairo",
"Clams Casino",]

c_rus_list_19 = [
"Claptone",
"Clara feat. RoseGold",
"Clara Louise feat. Fabian Buch",
"Clara Mae",
"Clara Sofie",
"Clare Maguire",
"Claremont & Askya",
"Clarence Gatemouth Brown",
"Claris & The Risk",
"Clarissa",
"Clarity Of Sound",
"Clark & Kent",
"Clark and Kent",
"Clark Kent feat. Mimi Page",
"Clark Owen feat. Лена Катина (ex. t.A.T.u)",
"Clark Sugar",
"Clase A",
"Clash",
"",
"Class",
"CLassic (ВУТОНН)",
"Classified feat. B.o.B",
"Classified feat. Olly Murs",
"Classix Nouveaux",
"Claud",
"Claude",
"Claude Chagall",
"Claude Ciari",
"Claude Daniel",
"Claude Daniel & Just-C",
"Claude feat. Frou Frou",
"Claude Kelly",
"Claude Vonstroke",
"Claudette",
"Claudette Ortiz",
"Claudette Pace",
"Claudette Peters",
"Claudia Beni",
"Claudia Cazacu",
"Claudia Cream",
"Claudia Faniello",
"Claudia Leitte",
"Claudia Lennear",
"Claudia Pascoal",
"Claudia Pavel",
"Claudia Rezende",
"Claudia Rusu",
"Claudia Sexxy",
"Claudia T.",
"Claudio & Gino & Mr.Slide",]

c_rus_list_20 = [
"Claudio Caccini feat. Carl",
"Claudio Colbert",
"Claudio Cristo",
"Claudio Mingardi",
"Claudio Rivera feat. Tony Ray",
"Claudio Tahi",
"Claudio Tuma",
"Claudiu Mirea",
"Claudiu Zamfira",
"Claus Backslash",
"Clavee",
"Clay C & Carla Werner",
"Claydee",
"Clean Bandit",
"Clean Vision",
"Clear Majeure",
"Clear Six feat. Brander",
"Clearmajeure",
"Cledy West",
"Clelia Felix",
"Clem Beatz feat. MIAE",
"Clem Leek",
"Clemens",
"Clement Bcx",
"Clement Leroux",
"Clement Marfo",
"Clementino",
"Cleo Laine",
"Cleopatra Stratan",
"Cleopold",
"Client Liaison",
"Clients",
"Cliff Neptune feat. Karenka",
"Cliff Richard",
"Cliff Stevens",
"Cliff Sweeney",
"Cliff Turner",
"Clifford White",
"Clifton Chenier",
"Climatic",
"Clint Black",
"Clint Mansell",
"Clint Mansell Feat. Kronos Qua",
"Clint Stewart",
"Clinton Sparks",
"Clion & Kamisory",
"CLIQ",
"Clive Stevens",
"Clixx feat. IAML",
"CLMD",]

c_rus_list_21 = [
"Clock On 5 ft. Joey Mauro",
"ClockTape feat. Matt Powell",
"Clockvice",
"Clokx",
"Cloonee",
"Clophelin feat. Владисlove Гайдовский",
"Closed Doors",
"Cloud 41 & Louis Moreau",
"Cloud 7",
"Cloud Break",
"Cloudchord",
"CloudNone",
"Clous Van Mechelen",
"Cloverdale",
"Cloves",
"Club 1600",
"Club 41 feat. Crazy Sir-G",
"Club Cheval",
"Club Corporate feat. Mouss MC",
"Club Crusaders",
"Club Jackers Project feat. IdeadEyE",
"Club Unique",
"Club Yoko",
"Clubaccess",
"Clubbasse",
"Clubfreakz",
"Clubhunte",
"Clubhunter",
"Clubraiders",
"Clubstone",
"Clubwaver",
"Clutch",
"Clyde Mcphatter",
"CMCS",
"CNCO",
"Co.Ro.",
"Coal Chamber",
"CoastCity & Luis Fonsi",
"Coastline",
"Coasts",
"Cobi Mike",
"Cobra Starship",
"Coburn vs. Destructo",
"Coca Dillaz",
"Coca Vango feat. Tyga",
"CockNBullKid",
"Coco Fay",
"Coco Fay feat. Jolie Lassen",
"Coco Jones",
"Coco Montoya",]

c_rus_list_22 = [
"Coco Morier",
"Coco O.",
"Cocogroove",
"Cocoon",
"Cocos",
"Cocosuma",
"Cocovan",
"Cod3x",
"Code Beat feat. Snoop Dogg, T.I. & Beat Frequency",
"Code Kunst feat. Lee Hi",
"Code Pandorum & Lord Swan3x",
"Code313 & Аля Кумар",
"Codeko",
"Codero",
"Cody Draiken",
"Cody Island",
"Cody Simpson",
"Coeur De Pirate",
"Coez",
"Coffee",
"Coffeeman",
"Coheed",
"Coin",
"CoJo",
"Col3trane feat. Djds & Raye",
"Cola Girl",
"Colbie Caillat",
"Colbie Caillat feat. Common",
"Colby O'Donis",
"Cold Blank feat. Veela",
"Cold Blue",
"Cold Face",
"Cold Fusion",
"Cold Grits",
"Cold In May",
"Cold Rush feat. Tiff Lacey",
"Cold Stone",
"Cold War Kids",
"Coldbeat & Guy Von James",
"Coldplay",
"Cole Plante",
"Colette Carr",
"Colin Crooks",
"Colin James",
"Colin Rouge & Stassie White",
"Colin Ward",
"Colina",]

c_rus_list_23 = [
"Coline",
"Coll3rk & Daav One",
"Collectif Metisse",
"Collective Soul",
"Colleen D'Agostino",
"",
"College Girls",
"Collin McLoughlin",
"Collin Selini feat. John Harris",
"Colombo",
"Colonel Bagshot",
"Colonel Loud feat. Too Short, Snoop Dogg & Ricco Barrino",
"Colonia",
"Colonial One feat. Eva Kade",
"Colony House",
"Colorado",
"Colour",
"Colouring",
"Colours Of Sound feat. Holly Rey",
"Colt Ford feat. Mitchell Tenpenny",
"Colton Dixon",
"Colton Ford",
"Com Truise",
"Coma Baby feat. Lyane Leigh",
"Coma Feat. Ltc",
"Comah",
"Combat Cars",
"Combination",
"Come’n'Done",
"Comets We Fall feat. Yushichi",
"Comic Gate vs Myon & Shane 54 feat. Aruna",
"Comiccon",
"Coming Soon!!! feat. Michele Adamson",
"Comis",
"Commercial Club Crew",
"Commodores",
"Common",
"Compact Disco",
"Compton Menace feat. Wiz Khalifa",
"Con Brio",
"Conan Gray",
"Conan Osiris",
"Conchita Wurst",
"Conect & Ivan Lexx",
"Confusious",
"Congorock & Clockwork",
"Congrats",
"Conjure One",
"Conkarah feat. Shaggy",
"ConKi & Tommy Kratch feat. Alea",
"Connect-R",
"Connells",
"Connie Francis",
"Connor Bvrns feat. Bonn",
"Conor Maynard",
"Conor Ross",
"Conrad Product",
"Conrad Sewell",
"Conrad Subs",
"Conro",]

c_rus_list_24 = [
"Consequence feat. Lupe Fiasco & Chris Turner",
"Consolerctrl",
"Consoul Trainin",
"Conspiracy",
"Constant Z",
"Constantin & Hardbros feat. Jonny Rose",
"Constantine",
"Constantinos Christoforou",
"Construction",
"Consuelo Costin",
"Contrabanda",
"Contrvbvnd X Kraeday",
"Conway The Machine feat. Eminem",
"Cookie Crushers",
"Cookie Monsta",
"Cookin' On 3 Burners",
"Cookzee",
"Cool & Station",
"Cool Cut",
"Cool Keedz",
"Cool Mike feat. Anna Montgomery",
"Cool project",
"Cool Sixth",
"Coolio",
"Coone feat. Bassjackers, Gldy LX",
"Cooops",
"Coop Capone feat. Wiz Khalifa & Juicy J",
"Cooper & Gatlin",
"Cooper Phillip",
"Cooperated Souls",
"Coopex",
"Copamore feat. Alvin River",
"Copy & Paste",
"Copy Club",
"Copycattz",
"Copyright feat. Ann Saunderson",
"Copyright feat. Shovell",
"Copyzor, Roland Boggio",
"Corado",
"Corderoy",
"Corey Andrew & Can Claas",
"Corey Antwone",
"Corey Chorus",
"Corey Gray",
"Corey James",
"Corey Taylor",
"Cori B. feat. Snoop Dogg",
"Corin C",
"Corina",
"Corinna May",]

c_rus_list_25 = [
"Corinne Bailey Rae",
"Coritsa",
"Corna",
"Corneille",
"Cornell Dupree",
"Corner, Miamisoul",
"Corner, Toygunz",
"Cornerstone",
"Corona",
"Corrado Saija",
"Correatown",
"Corroded",
"Corson",
"Cortes feat. Aurelian Temisan",
"Corti & Lamedica",
"Corti Organ",
"Cosculluela",
"Coska",
"Cosmic & Nilson",
"Cosmic Funk",
"Cosmic Gate",
"Cosmic Heaven",
"Cosmik",
"Cosmin Simionica",
"Cosmin Tzl",
"Cosmo",
"Cosmo Notes",
"Cosmo's Midnight",
"Cosmos & Creature",
"Cosmos Girls",
"Cosmos Midnight feat. Kucka",
"Cosmos Sound Club",
"Cosmosound",
"Cosmow",
"Costa",
"Costa Mee",
"Costa Pantazis",
"Costantino Toma",
"Costas Varras",
"Costero",
"Costi feat. Alix",
"Costi feat. Randy Class",
"Costi Ionita & Sahara",
"Costi x Emilia x Jay Maly",
"Costi, Drei Ros, Nastasia Griffin, Pack The Arcade, Bel, Kief Brown",
"Costi, Flama, King Blak",
"Cosy feat. Mellina",
"Cosy feat. Ruxandra Vidican",
"COTIS",
"Cottonmouth feat. Holly Grey",]

c_rus_list_26 = [
"Count Prince Miller",
"Count Suckle, Freddie Notes & The Rudies",
"Counter Point",
"Counting Crows",
"Country Girl",
"County Jels",
"Coupe & Anilasor",
"Couple",
"Courage",
"Couros feat. Alyss",
"Courrier",
"Courtland & Watson",
"Courtlin Jabrae feat. Lisa LoneWolf",
"Courtney Act",
"Courtney Argue",
"Courtney Bennett",
"Courtney feat. Flo Rida",
"Courtney Love",
"Courtney Noelle",
"Courtney Svendson",
"Cousin Stizz feat. City Girls",
"Covenants feat. GIA",
"Cover Drive",
"Cowsills",
"Coxwell",
"Coyot",
"Coyu",
"Cozmic",
"Cozy",
"Cozy Powell",
"Cr3on & Marcus feat. Gwendolyne",
"Craig Armstrong",
"Craig Cardiff",
"Craig Connelly",
"Craig David",
"Craig Joiner",
"Craig London feat. Lokka Vox",
"Craig Lounders",
"Craig Smart",
"Craig Williams",
"Cramp feat. Natalie Peris",
"Crankdat",
"Cranksters",
"Crasca",
"Crash",
"Crash feat. Pixy J",
"Crash Island",
"Crash и Кастро",
"Craspore",
"Craves feat. Ashe",]

c_rus_list_27 = [
"Craving",
"Cray",
"Crazibiza",
"Crazy Cousinz feat. Alex Mills",
"Crazy Frog",
"Crazy House",
"Crazy Monkey Gang",
"Crazy Town",
"Crazy Win",
"Crazy-T",
"CrazyBeats",
"CRBL",
"Creador De Fuego",
"Creation",
"Creative Ades",
"Creative Ades feat. Janethan",
"Creedence Clearwater Revival",
"Creep feat. Alpines",
"Creep feat. Dark Sister",
"Creep feat. Sia",
"Cres-One",
"Crest'One",
"CrestOne",
"Crew 7",
"Crew Cardinal",
"Crime Mob",
"Crime Spoons",
"Crime Zcene",
"CrImINaLль",
"Criminal Vibes",
"Crimson Apple",
"Crimson Black",
"Cris Cab",
"Cris Delanno",
"Cris Grey",
"Cris Hagman & Davi Lisboa",
"Cris Mario & Er Vyn feat. Sira",
"Cris Mario feat. Nicky",
"Criss & Ronny",
"Crissa N.",
"Crissy Criss & Wide Awake",
"Cristian Deluxe & Mr. Rommel",
"Cristian Lavino feat. Pol Rossignani",
"Cristian Lex",
"Cristian Marchi",
"Cristian Martin",
"Cristian Poow & Andrey Exx feat. Dennis Wonder",
"Cristian Tomas feat. Hybym",
"Cristian Varela",
"Cristian-Daniel",]

c_rus_list_28 = [
"Cristiano Matto feat. Gabriele",
"Cristina Balan",
"Cristina Croitoru",
"Cristina Dee",
"Cristina Scarlat",
"Cristina Spatar",
"Cristina Vasiu",
"Cristion D'Or & Fat Joe & De La Ghetto",
"Cristna",
"Cristoph",
"Cristyle",
"Critical Bill",
"Critika & Saik",
"Crius",
"Crizzly feat. Crichy Crich",
"CRNKN feat. Jhene Aiko",
"Croatia Squad",
"Crocadile",
"Crocodealer",
"Crocy",
"Cron",
"Crook MHD",
"Crookers",
"Cropper",
"Cross Medio",
"Crossnaders & Ale Mora feat. MC Gunner",
"Crossover",
"Crow Black Chicken",
"Crowded House",
"Crown The Empire",
"Crowne Troupe",
"Cruel Youth",
"Cruels feat. Salt Ashes",
"Crusada",
"Crush and Alexandra",
"Crush Atlantic",
"Crush Effect",
"Crush feat. Alexandra Ungureanu",
"Crux",
"Cruxx",
"Cruz Cafune",
"Crvvcks",
"Cry Solnca",
"Crysalis",
"Crystal Ball",
"Crystal Castles",
"Crystal Dreams",
"Crystal Fighters",
"Crystal Lake",
"Crystal Renee",]

c_rus_list_29 = [
"Crystal Rock",
"Crystal Shakers",
"Crystal Skies",
"Crystal Stilts",
"Crystal Waters",
"Crystallites",
"Crywolf",
"CRZY",
"Cseldj feat. Lynn",
"Cub Sport",
"Cuba Club",
"Cuban Link Feat. Mya",
"Cube 1 feat. Qwote & Pitbull",
"CubeTonic feat. Dilara Gadel",
"Cubicolor",
"CuckooLander",
"Cuco & Dillon Francis",
"Cue",
"Cueboy & Tribune",
"Cuebrick",
"Cugar",
"Cuja",
"Culcha Candela",
"Culiar",
"Cullen Bay",
"Culprate feat. CoMa & Koda",
"Culpriit",
"Cult Groove",
"Cult Of The Fox",
"Culture Beat",
"Culture Code",
"Culture Shock",
"CupcakKe",
"Cuppy feat. Sarkodie",
"Curacao",
"Curbi",
"Cureton",
"Cureton feat. Joegarratt",
"Curfew & Hopex",
"Curmit & Co",
"Currensy feat. August Alsina & Lil Wayne",
"Curro Pinana",
"Curses",
"Curtis Alto",
"Curtis Gabriel",
"Curtis Mayfield",
"Curtis Salgado",
"CUT",
"Cut Groove",
"Cutline feat. Belle Humble",]

c_rus_list_30 = [
"Cutline feat. Fleur",
"Cuurley & Kayda",
"Cuza & Irina Rimes feat. George Hora & Carmen Tanase",
"CVBZ",
"CVLI feat. PVRVDIGMV",
"CVLTVRE",
"Cvpellv",
"Cvpellv feat. Тимати",
"Cvsper",
"CXLOE",
"Cyantific",
"Cyantific feat. Benji",
"Cyber Space ft. Linda Jo Rizzo",
"Cyberx",
"Cygnus X",
"CYGO",
"Cymande",
"CYN",
"Cyndi Lauper",
"Cynthia Lissette",
"Cypress Hill",
"Cyran",
"Cyrenic",
"Cyril Caps",
"Cyril Hahn feat. Joel Ford",
"Cyril Neville",
"Cyril Pink feat. Llynn C",
"Cyril Ryaz",
"Cyrus",
"Czar",
"CZYK feat. Moe Phoenix",
"Cанн, Рем Дигга, Слеп Ро",
"Cборная Союза",
"Cлот",
]


litera = SoundSymbol.objects.get(name="C")

count = 0

for tag in c_rus_list_1:
    tracks = client.get('/tracks', q=tag, limit=page_size, linked_partitioning=1)
    if tracks:
        for track in tracks.collection:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            if track.description:
                description = track.description[:500]
            else:
                description=None
            try:
                Music.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                count = count + 1
        while tracks.next_href != None and count < 2000:
            tracks = client.get(tracks.next_href, limit=page_size, linked_partitioning=1)
            for track in tracks.collection:
                created_at = track.created_at
                created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                if track.description:
                    description = track.description[:500]
                else:
                    description=None
                try:
                    Music.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1
