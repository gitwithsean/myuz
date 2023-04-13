from noveller.models import *
from pprint import pprint
from django.db import transaction
from django.core.management.base import BaseCommand

content = {
  "setting": {
    "general_setting": [
      "this is set in medieval Ireland, in the first half of the 11th Century",
      "there is brutality, danger and trauma, but there is also beauty, nature, music, kindness and community.",
      "There are bards. druids, craftspeople, and storytellers. some of whom provide comfort, storytelling, examples of human tenderness, beauty and insight.",
      "There is a mixture of Christianity and Celtic/Pagan beliefs. The truly ancient sacred and divine places (e.g. Newgrange) make the stories of a son of god (Christ) from a faraway land harder to take seriously. The narrator is aware of this tension, however most of the characters are untroubled by their mixed holding of these beliefs.",
      "Each side (christian / pagan) does have militants who can cause trouble for our protagonists, but their beliefs make them easy to manipulate, and in some cases their beliefs make them helpful.",
      "The book draws from the political, social and environmental history of Ireland in those years. It also draws from ancient Irish mythology.",
      "The growing port of Dublin (Dubh Linn), the building of Christchurch Cathedral there.",
      "The story The Cattle Raid of Cooley (Táin Bó Cúailnge) dates back to the Iron Age, but its written form in Old Irish was likely created in the 11th or 12th century. It was a very popular epic tale of rivalry, war, and heroism"
    ]
  },
  "deeper_background_research": [
    {
      "uuid": "dbr001",
      "topic": "Brehon Law (Fenechas)",
      "notes": [
        "legal system used in Ireland up until the 12th century",
        "roots in Celtic, pre-Christian society of Ireland",
        "named after the Brehons, the judges and legal scholars responsible for interpreting and preserving laws.",
        "originally transmitted orally by highly trained legal professionals",
        "written down in Old Irish during the early Christian period, as early as the 7th century",
        "Brehon Laws treated women with more respect and provided them with more rights compared to other contemporary legal systems",
        "Could inherit and hold property",
        "participate in legal contracts",
        "seek divorce or separation",
        "As a business owner, she would be considered a \"ban-aírech\" or female landholder, granting her certain rights and protections",
        "able to represent herself and seek the assistance of a Brehon, or a judge, to settle the matter according to the Brehon Laws.",
        "The Brehon Laws recognized different forms of marriage, with varying degrees of property rights and obligations for both spouses"
      ]
    },
    {
      "uuid": "dbr002",
      "topic": "Work and Lifestyle",
      "notes": [
        "most lived in rural settlements, with their lives centered around agriculture",
        "growing crops such as oats, barley, and wheat",
        "raised livestock, including cattle, sheep, and pigs. The wealth of a family was often measured by the number of cattle they owned."
      ]
    },
    {
      "uuid": "dbr003",
      "topic": "Entertainment and Sports",
      "notes": [
        "hurling",
        "horse racing",
        "wrestling",
        "various forms of stick fighting",
        "music",
        "poetry",
        "storytelling",
        "Bards and harpists were highly regarded in society",
        "they traveled from settlement to settlement, sharing tales of history, ythology, and romance."
      ]
    },
    {
      "uuid": "dbr004",
      "topic": "Social Hierarchy",
      "notes": [
        "The Gaelic social structure was hierarchical",
        "the nobility and landowners at the top",
        "followed by freemen (commoners)",
        "and finally unfree laborers and slaves"
      ]
    },
    {
      "uuid": "dbr005",
      "topic": "Family",
      "notes": [
        "most important social unit in early 11th century Ireland",
        "extended families often living together in clusters of houses called \"clachans\"",
        "clachans typically consisted of a few houses built around a central area used for communal activities"
      ]
    },
    {
      "uuid": "dbr006",
      "topic": "Politics",
      "notes": [
        "society was organized into a system of tuatha (small indepedenent kingdoms)",
        "tuatha were often in conflice with each other",
        "Warfare provided an opportunity for warriors to gain prestige and wealth, as they would be rewarded with land and cattle"
      ]
    },
    {
      "uuid": "dbr007",
      "topic": "Religion",
      "notes": [
        "Ireland was known throughout Europe for its monastic settlements, which served as centers of learning and scholarship.",
        "Monks preserved and copied ancient manuscripts, ensuring the survival of important historical and religious texts",
        "Offered education for a price that only the children of nobility could afford"
      ]
    },
    {
      "uuid": "dbr008",
      "topic": "Education",
      "notes": [
        "religious texts",
        "Brehon laws",
        "latin",
        "Gaelic",
        "Old Irish",
        "history",
        "poetry",
        "Monastic schools attracted students from across Europe, making Ireland a hub of learning and scholarship during this time."
      ]
    },
    {
      "uuid": "dbr009",
      "topic": "Economy and Trade",
      "notes": [
        "agriculture",
        "craftwork",
        "trade",
        "pottery",
        "metalwork",
        "textiles",
        "exports:  wool, hides, and livestock",
        "imports: wine, salt, and luxury items such as silk and spices"
      ]
    },
    {
      "uuid": "dbr010",
      "topic": "Fairs and Fesitvals",
      "notes": [
        "important social events in early 11th century Ireland",
        "trade opportunities",
        "entertainment",
        "settling of legal disputes",
        "Samhain",
        "Bealtaine"
      ]
    }
  ],
  "character_related_setting_info": [
    {
      "uuid": "crs001",
      "name": "Settings as it relates to Young Lady Eabha",
      "character": {
        "uuid": "001",
        "name": "Young Lady Eabha",
        "version": 2,
        "description": "proprieter of a pub in Dubh Linn, and in a marriage of convenience with an older gay man"
      },
      "rights": [
        "Brehon Laws treated women with more respect and provided them with more rights compared to other contemporary legal systems",
        "Could inherit and hold property",
        "participate in legal contracts",
        "seek divorce or separation",
        "As a business owner, she would be considered a \"ban-aírech\" or female landholder, granting her certain rights and protections",
        "able to represent herself and seek the assistance of a Brehon, or a judge, to settle the matter according to the Brehon Laws.",
        "The Brehon Laws recognized different forms of marriage, with varying degrees of property rights and obligations for both spouses",
        "the Viking settlement of Dubh Linn (Dublin) was influenced not only by the Brehon Laws but also by Norse laws and customs. The young woman\\'s legal status and rights would be affected by the interplay of these two legal systems"
      ],
      "appearance_modifiers": {
        "clothing": [
          "long dress made of wool or linen",
          "dyed with natural colors",
          "belt at the waist",
          "woolen cloak or shawl for warmth and protection against the elements",
          "simple leather shoes or boots"
        ],
        "hair_head_options": [
          "long and loose",
          "braided and pinned up",
          "simple headcovering, such as a linen cap or a scarf"
        ],
        "perfume": "",
        "makeup": "",
        "shaving": "",
        "washing_schedule": ""
      },
      "attitudes": [],
      "leisure": [
        "fidchell (board game)",
        "singing",
        "dancing",
        "storytelling",
        "conversing with the diverse set of customers at the pub"
      ],
      "food": [
        "oat and barley porridge",
        "dairy products such as cheese and butter",
        "vegetables like cabbage, onions, and leeks",
        "fruits like apples, plums, and berries",
        "meat, usually pork or beef, was usually for feasts and special occasions.",
        "pub work gives her a little more diversity than others"
      ],
      "work": [
        "responsible for managing the day-to-day operations, including overseeing the production and sale of ale, mead, and other beverages, as well as the procurement of food and provisions",
        "her status as a business owner would garner her a degree of respect within the community."
      ],
      "social_life": [
        "Her establishment would be a gathering place for locals and travelers alike, offering a warm atmosphere, hearty fare, and lively entertainment, such as storytelling and music.",
        "Despite having more equal rights under Brehon law, her social standing would still be largely influenced by her marital status and family connections."
      ]
    },
    {
      "uuid": "crs002",
      "name": "Setting as it relates to Teenage Mac Bais",
      "character": {
        "uuid": "002",
        "name": "Teenage Mac Bais",
        "version": 2,
        "description": "Young male scholar of Brehon law, living in Dubh Linn"
      },
      "rights": [],
      "appearance_modifiers": {
        "clothing": [
          "made of wool",
          "a léine, a long tunic reaching down to his knees or ankles",
          "dyes in natural color",
          "a woolen cloak, fastened at the shoulder with a brooch, to protect him from the elements",
          "simple leather shoes or boots."
        ],
        "hair_head_options": [
          "short, cropped hair",
          "bowl cut"
        ],
        "perfume": "",
        "makeup": "",
        "shaving": "scruffy teenage boy hair",
        "washing_schedule": ""
      },
      "attitudes": [],
      "leisure": [
        "fidchell (board game)"
      ],
      "food": [
        "oat and barley porridge",
        "dairy products such as cheese and butter",
        "vegetables like cabbage, onions, and leeks",
        "fruits like apples, plums, and berries",
        "meat, usually pork or beef, was usually for feasts and special occasions.",
        "but living over a pub gives him a little more diversity than others"
      ],
      "work": [
        "under the tutelage of a respected Brehon",
        "expected to show respect and deference to his teacher",
        "daily lessons with his Brehon teacher",
        "from property rights and contracts to criminal offenses and penalties.",
        "expected to memorize the laws and their intricacies, as the Brehon Laws were an oral tradition, passed down from one generation to the next.",
        "apprenticed with a more experienced Brehon after his education, applying his knowledge to real world scenarios",
        "Eventually, he becomes a Brehon in his own right, responsible for upholding justice and maintaining social order within his community.",
        "His decisions and rulings would shape the lives of those around him, ensuring the continued stability of the society he served."
      ],
      "social_life": [
        "The pub would be a gathering place for locals and travelers alike, offering a warm atmosphere, hearty fare, and lively entertainment, such as storytelling and music.",
        "gradually gain respect and recognition from the community as he progressed in his Brehon law studies.",
        "people would seek his guidance in resolving disputes and interpreting the law."
      ]
    }
  ],
  "background_events": [
    {
      "uuid": "be001",
      "event": "Battle of Clontarf",
      "year": 1014.3
    },
    {
      "uuid": "be002",
      "event": "Plague strikes Dubh Linn and Leinster",
      "year": 1015
    },
    {
      "uuid": "be003",
      "event": "Power struggle between various Irish kingdoms and the Norse-Gaelic Vikings.",
      "year": {
        "from": 960,
        "to": 1080
      }
    },
    {
      "uuid": "be004",
      "event": "Viking raids",
      "year": {
        "from": 960,
        "to": 1080
      }
    },
    {
      "uuid": "be005",
      "event": "Growth of Viking Settlements as trade centers",
      "year": {
        "from": 960,
        "to": 1080
      }
    },
    {
      "uuid": "be006",
      "event": "Battle of Tara",
      "year": 980
    }
  ],
  "main_characters": [
    {
      "name": "Éabha",
      "uuid": "001",
      "age_at_start": "14",
      "gender": "female",
      "origin": "kidnapped by Viking slavers, sold into marriage at 12 to a 37 year old blacksmith, has not yet borne children for him and for that she is beaten every day",
      "representative_of": [
        "Irish name that means \"living\"",
        "life",
        "growth",
        "nurture",
        "survival (despite a world that makes living seem not worth it (a cruel and torturous state of being.)"
      ],
      "permanent_characteristics": [
        ""
      ],
      "character_versions": [
        {
          "version": 1,
          "version_name": "teenage",
          "age_range_for_this_version": {
            "age_range_start": 14,
            "age_range_end": 19
          },
          "locations": [
            {
              "uuid": "l100",
              "name": "The Village",
              "rel": "community"
            },
            {
              "uuid": "l101",
              "name": "The Forge",
              "rel": "home"
            }
          ],
          "preferred_weapon": "manipulation",
          "appearance": {
            "distinguishing_features": [
              "diamond shaped birthmark on right temple"
            ],
            "eyes": "blue/grey",
            "hair": "fair",
            "face": "oval",
            "build": "slender, broad shouldered",
            "movement": "caerful, measured"
          },
          "strengths": [
            "socially connected",
            "empathetic",
            "nurturing",
            "willful",
            "scheming",
            "surviving",
            "spiritual",
            "mentally strong",
            "practical",
            "able to navigate the world of men",
            "telling lies",
            "manipulation",
            "predictive/portentious dreams?",
            "pain/suffering threshold"
          ],
          "weaknesses": [
            "physical strength",
            "PTSD flashbacks",
            "nightmares",
            "a beauty that draws the attention of rapacious men",
            "alcohol"
          ],
          "other_aspects": [
            "bears grudges",
            "doesn\\'t give back trust easily/at all"
          ],
          "often_perceived_as": [
            "manipulative",
            "uppity",
            "charming",
            "sweet",
            "tough"
          ],
          "drives": [
            "protecting Mac Báis",
            "survival",
            "revenge",
            "a lasting peace"
          ],
          "fears": [
            "Mac Báis being left alone"
          ],
          "beliefs": [],
          "internal_conflicts": [],
          "subter": "",
          "relationships": [
            {
              "uuid": "002",
              "name": "Mac Bais",
              "age_it_started": 14,
              "rel": [
                "protector",
                "adoptive sister/mother"
              ]
            },
            {
              "uuid": "003",
              "name": "The Blacksmith",
              "age_it_started": 12,
              "rel": [
                "wife",
                "victim",
                "target of vengeance"
              ]
            },
            {
              "uuid": "004",
              "name": "Travelling Bard",
              "age_it_started": 18,
              "rel": [
                "fling",
                "muse"
              ]
            }
          ]
        },
        {
          "version": 2,
          "version_name": "young lady",
          "age_range_for_this_version": {
            "age_range_start": 19,
            "age_range_end": 23
          },
          "changes_from_previous_version": {
            "preferred_weapon": "manipulation",
            "locations": [
              {
                "uuid": "l103",
                "name": "Dubh Linn",
                "rel": "community"
              },
              {
                "uuid": "l104",
                "name": "The Burning Boat",
                "rel": "home"
              },
              {
                "uuid": "l102",
                "name": "Room over The Burning Boat",
                "rel": "workplace"
              }
            ]
          }
        }
      ]
    },
    {
      "name": "Mac Báis",
      "uuid": "002",
      "age_at_start": "5",
      "gender": "male",
      "origin": "unclear to the reader and the people in his life. Child/descendent of a witch doctor who was kidnapped by Vikings from a far away land (Newfoundland, on the American continent) brought back to Viking lands, and then to Ireland.\n\nHe is mixed race with Native American/Norse-Irish (so he looks strange, but not totally foreign)\n\nIts theorized many autistic people in ancient/medieval times were considered witches, doctors, seers, etc.\n\nAutism is inheritable, so his forebears on his mother\\'s side were a lineage of Newfoundland Native American witch doctors (all autistic).",
      "representative_of": [
        "not a real name, but can be translated as \"Son of Death\"",
        "banality, neutrality, inevitability and necessity of death",
        "the need for death to make playfulness, beauty, youth and renewal"
      ],
      "permanent_characteristics": [
        "autistic"
      ],
      "character_versions": [
        {
          "version": 1,
          "version_name": "child",
          "age_range_for_this_version": {
            "age_range_start": 5,
            "age_range_end": 9
          },
          "locations": [
            {
              "uuid": "l100",
              "name": "The Village",
              "rel": "community"
            },
            {
              "uuid": "l101",
              "name": "The Blacksmith\\'s House",
              "rel": "home"
            }
          ],
          "preferred_weapon": "knife",
          "appearance": {
            "distinguishing_features": [
              "mixed race with Native American/Norse-Irish features"
            ],
            "eyes": "dark brown",
            "hair": "black",
            "face": "oval",
            "build": "slender, agile",
            "movement": "quiet, swift"
          },
          "strengths": [
            "neutral",
            "unconcerned",
            "sensitive",
            "coolly hyper-aware of danger",
            "unflappable",
            "pattern recognition",
            "intuitively expert killer",
            "academics",
            "agile",
            "quiet",
            "fearlessness"
          ],
          "weaknesses": [
            "socially oblivious",
            "physical strength",
            "pain/suffering threshold",
            "unconcerned with self-preservation",
            "planning",
            "scheming",
            "improvisation",
            "emotional control"
          ],
          "other_aspects": [
            "autistic (not ever mentioned in the story, but his behaviour and his perception and his relationships are led by that)",
            "part foreign"
          ],
          "often_perceived_as": [
            "something different",
            "holy",
            "mystical",
            "evil",
            "otherworldly",
            "inhuman",
            "demonic",
            "\"touched\"",
            "soft",
            "dumb"
          ],
          "drives": [
            "curiosity",
            "protecting Éabha",
            "learning"
          ],
          "fears": [
            "being left alone",
            "losing Éabha"
          ],
          "relationships": [
            {
              "uuid": "001",
              "name": "Éabha",
              "age_it_started": 5,
              "rel": [
                "protector",
                "adoptive brother/son"
              ]
            },
            {
              "uuid": "003",
              "name": "The Blacksmith",
              "age_it_started": 5,
              "rel": [
                "ward",
                "target of vengeance"
              ]
            }
          ]
        },
        {
          "version": 2,
          "version_name": "adolescent",
          "age_range_for_this_version": {
            "age_range_start": 9,
            "age_range_end": 17
          },
          "locations": [
            {
              "uuid": "l103",
              "name": "Dubh Linn",
              "rel": "community"
            },
            {
              "uuid": "l101",
              "name": "The Blacksmith\\'s House",
              "rel": "home"
            }
          ],
          "changes_from_previous_version": {
            "preferred_weapon": "bow and arrow",
            "strengths": [
              "stealth",
              "strategic thinking",
              "increased physical strength"
            ],
            "weaknesses": [
              "growing pains",
              "awkwardness during growth spurts"
            ],
            "relationships": [
              {
                "uuid": "004",
                "name": "Travelling Bard",
                "age_it_started": 14,
                "rel": [
                  "friend",
                  "teacher",
                  "source of inspiration"
                ]
              }
            ]
          }
        },
        {
          "version": 3,
          "version_name": "young adult",
          "age_range_for_this_version": {
            "age_range_start": 17,
            "age_range_end": 23
          },
          "changes_from_previous_version": {
            "preferred_weapon": "sword",
            "locations": [
              {
                "uuid": "l103",
                "name": "Dubh Linn",
                "rel": "community"
              },
              {
                "uuid": "l104",
                "name": "The Burning Boat",
                "rel": "home"
              },
              {
                "uuid": "l102",
                "name": "Room over The Burning Boat",
                "rel": "workplace"
              }
            ],
            "strengths": [
              "leadership",
              "matured combat skills",
              "refined strategy"
            ],
            "weaknesses": [
              "increased emotional vulnerability"
            ],
            "relationships": [
              {
                "uuid": "005",
                "name": "Éabha\\'s Husband",
                "age_it_started": 20,
                "rel": [
                  "friend",
                  "family"
                ]
              }
            ]
          }
        },
        {
          "version": 4,
          "version_name": "adult",
          "age_range_for_this_version": {
            "age_range_start": 23,
            "age_range_end": 30
          },
          "changes_from_previous_version": {
            "preferred_weapon": "spear",
            "strengths": [
              "expertise in multiple weapons",
              "greater emotional control"
            ],
            "weaknesses": [
              "physical decline",
              "growing world-weariness"
            ],
            "relationships": []
          }
        }
      ]
    }
  ],
  "main_characters_relationship": "Éabha and Mac Báis are a yin-yang pairing, orphans of the indifferent universe. they protect each other, love each other, cannot exist without the other, each has a darkness that is lit by a light in the other, each has a light that is consumed by the darkens in the other.Neither of them are good - nor are they bad. they are survivors. sometimes the price others have to pay for their survival is questionable",
  "secondary_characters": [
    {
      "name": "The Blacksmith",
      "uuid": "003",
      "age_at_start": "39",
      "origin": "Husband to Éabha",
      "preferred_weapon": "hammer",
      "strengths": [
        "physical strength",
        "powerful in his community"
      ],
      "weaknesses": [
        "bitter",
        "angry",
        "selfish",
        "not clever",
        "friendless"
      ],
      "representative_of": [],
      "other_aspects": [
        "abuser",
        "petty",
        "blames everyone but himself"
      ],
      "often_perceived_as": [
        "troubling",
        "socially powerful",
        "useful"
      ],
      "drives": [
        "greedy",
        "having a son"
      ],
      "fears": [
        "being seen as weak"
      ],
      "relationships": [
        {
          "uuid": "001",
          "name": "Eabha",
          "rel": [
            "husband",
            "abuser"
          ]
        },
        {
          "uuid": "002",
          "name": "Mac Bais",
          "rel": [
            "adoptive father",
            "target of vengeance"
          ]
        }
      ]
    },
    {
      "name": "Travelling Bard",
      "uuid": "004",
      "age_at_start": "16",
      "origin": "Visited the Village to tell stories",
      "preferred_weapon": "disarming charm",
      "strengths": [
        "storytelling",
        "charming",
        "handsome",
        "funny",
        "light",
        "intelligent"
      ],
      "weaknesses": [
        "physical strength",
        "naieve",
        "poor",
        "rootless"
      ],
      "representative_of": [],
      "other_aspects": [
        "philosophical",
        "friendly",
        "tragically romantic"
      ],
      "often_perceived_as": [
        "entraining",
        "a tourist in other people\\'s lives",
        "whimsicle"
      ],
      "drives": [
        "exploring",
        "travelling"
      ],
      "fears": [
        "being bored",
        "being perceived as boring"
      ],
      "relationships": [
        {
          "uuid": "001",
          "name": "Eabha",
          "rel": [
            "lover",
            "inspired by"
          ]
        },
        {
          "uuid": "002",
          "name": "Mac Bais",
          "rel": [
            "friend",
            "mentor"
          ]
        }
      ]
    }
  ],
  "characters": [
    {
      "uuid": "000",
      "name": "The Narrator"
    },
    {
      "uuid": "001",
      "name": "Eabha"
    },
    {
      "uuid": "002",
      "name": "Mac Bais"
    },
    {
      "uuid": "003",
      "name": "The Blacksmith"
    },
    {
      "uuid": "004",
      "name": "The Travelling Bard"
    },
    {
      "uuid": "005",
      "name": "Eabha\\'s Husband of Convenience"
    },
    {
      "uuid": "006",
      "name": "Brehon Law Mentor"
    }
  ],
  "locations": [
    {
      "uuid": "l100",
      "location": "The Village"
    },
    {
      "uuid": "l101",
      "location": "The Forge/Blacksmith\\'s House"
    },
    {
      "uuid": "l102",
      "location": "Rooms over \"The Burning Boat\""
    },
    {
      "uuid": "l103",
      "location": "Dubh Linn"
    },
    {
      "uuid": "l104",
      "location": "\"The Burning Boat\""
    },
    {
      "uuid": "l105",
      "location": "Clontarf"
    },
    {
      "uuid": "l000",
      "location": "On the Road"
    },
    {
      "uuid": "l999",
      "location": "Nowhere"
    }
  ],
  "story_events": [
    {
      "uuid": "se000",
      "themes": [
        "Dream"
      ],
      "location_uuid": "l999",
      "character_uuids": [
        "001"
      ],
      "description": "ooohhhhhhh",
      "year": "null"
    },
    {
      "uuid": "se001",
      "themes": [
        "Meeting"
      ],
      "location_uuid": "l105",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "Mac Bais and Eabha meet in the aftermath of the battle of Clontarf",
      "when": 1014.03
    },
    {
      "uuid": "se002",
      "themes": [
        "Acceptance"
      ],
      "location_uuid": "l101",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "The Blacksmith accepts Mac Bais into his home",
      "year": 1014.03
    },
    {
      "uuid": "se003",
      "themes": [
        "Abuse"
      ],
      "location_uuid": "l101",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "The Blacksmith realizes Mac Bais is \"useless\" and becomes increasingly abusive",
      "year": {
        "from": 1014.03,
        "to": 1014.11
      }
    },
    {
      "uuid": "se004",
      "themes": [
        "Time Passes"
      ],
      "location_uuid": "l100",
      "character_uuids": [
        "003"
      ],
      "description": "The town goes through events, harvests, church growing in power, Viking raids, more work for The Blacksmith",
      "year": {
        "from": 1015.1,
        "to": 1019
      }
    },
    {
      "uuid": "se005",
      "themes": [
        "Awareness"
      ],
      "location_uuid": "l100",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "Éabha becomes more aware of her strengths and finds friends with young people in The Village",
      "year": {
        "from": 1015.1,
        "to": 1019.4
      }
    },
    {
      "uuid": "se006",
      "themes": [
        "Festival"
      ],
      "location_uuid": "l100",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "Wandering Bard visits The Village for Bealtaine festival, Eabha has an affair with the bard",
      "year": 1019.5
    },
    {
      "uuid": "se007",
      "themes": [
        "Confrontation"
      ],
      "location_uuid": "l101",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "Confrontation between The Blacksmith and Eabha (Samhain), Mac Bais intervenes and his violent nature is revealed",
      "year": 1019.1
    },
    {
      "uuid": "se008",
      "themes": [
        "Escape"
      ],
      "location_uuid": "l100",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "Eabha and Mac Bais flee",
      "year": 1019.11
    },
    {
      "uuid": "se009",
      "themes": [
        "Hardship"
      ],
      "location_uuid": "l000",
      "character_uuids": [
        "001",
        "002"
      ],
      "description": "The winter of 1019/20 is hard on them in their fugitive life",
      "year": {
        "from": 1019.11,
        "to": 1020.1
      }
    },
    {
      "uuid": "se010",
      "themes": [
        "Settled"
      ],
      "location_uuid": "l103",
      "character_uuids": [
        "001",
        "002",
        "005",
        "006"
      ],
      "description": "Fast forward 5 years. Comfortable and established, Eabha is managing a bar \"The Burning Boat\" owned by her new husband (he\\'s gay, it is a marriage of convenience). Mac Bais is a young scholar of the Brehon Laws",
      "year": 1025
    }
  ],
  "style_guides": [
    {
      "uuid": "sg000",
      "name": "The Narrator\\'s Style Guide"
    },
    {
      "uuid": "sg001",
      "name": "Teenage Eabha\\'s 1st Person Narrative Style Guide"
    },
    {
      "uuid": "sg002",
      "name": "Infant Mac Bais\\' 1st Person Narrative Style Guide"
    }
  ],
  "factions": [
    {
      "uuid": "fa001",
      "name": "Vikings"
    },
    {
      "uuid": "fa002",
      "name": "Christian Zealots"
    },
    {
      "uuid": "fa003",
      "name": "Pagan Zealots"
    },
    {
      "uuid": "fa004",
      "name": "Brehons"
    },
    {
      "uuid": "fa005",
      "name": "Leinster Kings"
    },
    {
      "uuid": "fa006",
      "name": "Ulster Kings"
    },
    {
      "uuid": "fa007",
      "name": "Norse-Irish"
    }
  ],
  "chapters": [
    {
      "uuid": "chp001",
      "chapter_num": 1
    },
    {
      "uuid": "chp002",
      "chapter_num": 2
    },
    {
      "uuid": "chp002",
      "chapter_num": 3
    },
    {
      "uuid": "chp004",
      "chapter_num": 4
    },
    {
      "uuid": "chp005",
      "chapter_num": 5
    }
  ],
  "chapter_parts": [
    {
      "uuid": "chprt001",
      "name": "Chapter 1 - Part 1",
      "chapter": 1,
      "part": 1
    },
    {
      "uuid": "chprt002",
      "name": "Chapter 1 - Part 2",
      "chapter": 1,
      "part": 2
    },
    {
      "uuid": "chprt003",
      "name": "Chapter 1 - Part 3",
      "chapter": 1,
      "part": 3
    },
    {
      "uuid": "chprt004",
      "name": "Chapter 2 - Part 1",
      "chapter": 1,
      "part": 1
    },
    {
      "uuid": "chprt005",
      "name": "Chapter 2 - Part 2",
      "chapter": 2,
      "part": 2
    },
    {
      "uuid": "chprt006",
      "name": "Chapter 2 - Part 3",
      "chapter": 2,
      "part": 3
    },
    {
      "uuid": "chprt007",
      "name": "Chapter 3 - Part 1",
      "chapter": 3,
      "part": 1
    },
    {
      "uuid": "chprt008",
      "name": "Chapter 3 - Part 2",
      "chapter": 3,
      "part": 2
    },
    {
      "uuid": "chprt009",
      "name": "Chapter 3 - Part 3",
      "chapter": 3,
      "part": 3
    },
    {
      "uuid": "chprt010",
      "name": "Chapter 3 - Part 4",
      "chapter": 3,
      "part": 4
    },
    {
      "uuid": "chprt011",
      "name": "Chapter 5",
      "chapter": 5,
      "part": 0
    }
  ],
  "themes": [
    {
      "uuid": "th001",
      "name": "violence and youth"
    },
    {
      "uuid": "th002",
      "name": "death and life"
    },
    {
      "uuid": "th003",
      "name": "innocence"
    },
    {
      "uuid": "th004",
      "name": "vulnerability"
    }
  ],
  "chapter_part_summary": [
    {
      "uuid": "chprtsum0001",
      "section": "Lengthy description of the field in the battle\\'s aftermath"
    },
    {
      "uuid": "chprtsum0002",
      "section": "Mac Bais is wandering around the battlefield, looking around in childish (autistic) wonder"
    },
    {
      "uuid": "chprtsum0003",
      "section": "Mac Bais kills for the first time here as a dying man grabs him and hold on to him"
    },
    {
      "uuid": "chprtsum0004",
      "section": "Mac Bais is unbothered by the scene"
    },
    {
      "uuid": "chprtsum0005",
      "section": "Eabha is there, looting the dead by her husband\\'s order"
    },
    {
      "uuid": "chprtsum0006",
      "section": "Eabha notices Mac Bais , they interact, bond, and she takes him with her back home."
    },
    {
      "uuid": "chprtsum0007",
      "section": "get his first person perspective of the above from the moments after the man dies"
    },
    {
      "uuid": "chprtsum0008",
      "section": "after leaving the battlefield he relives his first permanent memory, killing the man and meeting Eabha"
    },
    {
      "uuid": "chprtsum0009",
      "section": "he is completely neutral about the killing, it was a puzzle to solve and he solved it"
    },
    {
      "uuid": "chprtsum0010",
      "section": "but has a new feeling that he hasn\\'t experienced before for Eabha (love)"
    },
    {
      "uuid": "chprtsum0013",
      "section": "The Blacksmith is working alone at the forge, which is also their home"
    },
    {
      "uuid": "chprtsum0014",
      "section": "Descriptive content: the experiences and emotions of being a blacksmith, the sounds, smells, temperatures, injuries, dangers, hardness, satisfaction, boredom, banality of the work"
    },
    {
      "uuid": "chprtsum0015",
      "section": "Waiting for Eabha\\'s return, he had sent her to the aftermath of the battle to loot for anything valuable that he could smith into jewelry to sell."
    },
    {
      "uuid": "chprtsum0016",
      "section": "We get an insight into his mind, his bitter thoughts and emotions, hints at why he feels this way but don\\'t go into detail, he is filled with excuses for not living the life he wants, blaming others. He hates everyone and everything, and feels he has good reason to."
    },
    {
      "uuid": "chprtsum0017",
      "section": "currently working on making farm tools - he hates the banality of this work."
    },
    {
      "uuid": "chprtsum0018",
      "section": "Embittered by Éabha\\'s inability to bear children, he spent everything he had on buying her from the slavers. There is no evidence the fertility problem does not lie with him."
    },
    {
      "uuid": "chprtsum0019",
      "section": "looking forward to the enjoyment of receiving the valuables Éabha\\' has discovered, or the satisfaction of beating her for not finding anything worth the time she spent looking."
    },
    {
      "uuid": "chprtsum0020",
      "section": "this part ends with The Blacksmith noticing the silhouette of two children emerging over the horizon"
    },
    {
      "uuid": "chprtsum0021",
      "section": "Mac Bais and Eabha approach The Forge"
    },
    {
      "uuid": "chprtsum0022",
      "section": "Eabha has been worrying about The Blacksmith\\'s reaction"
    },
    {
      "uuid": "chprtsum0023",
      "section": "Eabha is relieved that he is happy with her for the gift of this boy child she has brought back"
    },
    {
      "uuid": "chprtsum0024",
      "section": "he vows to be a more gentle and tender husband, and good father"
    },
    {
      "uuid": "chprtsum0025",
      "section": "he is playful with Mac Bais and offers to make them food"
    },
    {
      "uuid": "chprtsum0026",
      "section": "the scene as they enter the forge, their home, is gentle, comfortable, serene"
    },
    {
      "uuid": "chprtsum0027",
      "section": "Eabha is relieved they haven\\'t been beaten."
    },
    {
      "uuid": "chprtsum0028",
      "section": "In the mental and emotional space that this relief has opened up in her, her mind wanders"
    },
    {
      "uuid": "chprtsum0029",
      "section": "and lands on a repressed anger, fury, desire for revenge against The Blacksmith"
    },
    {
      "uuid": "chprtsum0030",
      "section": "she locks it away, she knows where it is, and knows that some day, with Mac Bais, she will be able to release it"
    },
    {
      "uuid": "chprtsum0025",
      "section": "Leaving the new found serenity of The Forge, begin an evocative description of The Blacksmith\\'s Village and its inhabitants as it passes from Spring into Fall"
    },
    {
      "uuid": "chprtsum0026",
      "section": "Return to The Forge approaching winter, it is a much less serene scene than The Forge we left in Spring"
    },
    {
      "uuid": "chprtsum0027",
      "section": "Mac Bais finds Eabha angry and tearful, but not crying, washing clothes in the brook that passes through their land."
    },
    {
      "uuid": "chprtsum0028",
      "section": "It is close to Winter, the blacksmith\\'s initial warmth has faded."
    },
    {
      "uuid": "chprtsum0029",
      "section": "It is clear now that the boy is in some way different (autistic), he will never make a good husband, bring a good dowry, work the blacksmith\\'s shop, or be useful in any way to The Blacksmith."
    },
    {
      "uuid": "chprtsum0030",
      "section": "The Blacksmith hasn\\'t said any of this, but Eabha has read it in him."
    },
    {
      "uuid": "chprtsum0031",
      "section": "He grows jealous of the bond between Eabha and Mac Bais, and increasingly takes his anger out on Éabha."
    },
    {
      "uuid": "chprtsum0032",
      "section": "Mac Bais, initially oblivious of the increasing abuse, eventually senses Éabha\\'s distress."
    },
    {
      "uuid": "chprtsum0033",
      "section": "He starts to notice feelings of protectiveness over her."
    },
    {
      "uuid": "chprtsum0034",
      "section": "Mac Bais deduces that Eabha is abused because there is something wrong with him that makes The Blacksmith angry."
    },
    {
      "uuid": "chprtsum0035",
      "section": "Mac Bais attempts to mask those parts of himself."
    },
    {
      "uuid": "chprtsum0036",
      "section": "After a few months of masking the traits in him that trouble The Blacksmith, he finds Eabha angry and tearful, but not crying, washing clothes in the brook that passes through their land."
    },
    {
      "uuid": "chprtsum0037",
      "section": "she has an injury from The Blacksmith"
    },
    {
      "uuid": "chprtsum0038",
      "section": "Mac Bais finds a new feeling in him he has never felt before, destructive fury"
    }
  ],
  "chapter_outlines": [
    {
      "uuid": "cho001",
      "story_event": {
        "uuid": "se001"
      },
      "chapter": {
        "uuid": "chp001",
        "chapter_num": 1
      },
      "summary": "Mac Bais and Eabha meet in the aftermath of the battle of Clontarf (Dublin, Ireland, year 1014).",

        "parts": [
          {
            "uuid": "chprt001",
            "name": "Chapter 1 - Part 1",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l105",
              "description": "Clontarf"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              }
            ],
            "themes": [
              {
                "uuid": "th001",
                "name": "violence and youth"
              },
              {
                "uuid": "th002",
                "name": "death and life"
              },
              {
                "uuid": "th003",
                "name": "innocence"
              },
              {
                "uuid": "th004",
                "name": "vulnerability"
              }
            ],
            "factions": [
              {
                "uuid": "fa001",
                "name": "Vikings"
              },
              {
                "uuid": "fa005",
                "name": "Leinster Kings"
              },
              {
                "uuid": "fa006",
                "name": "Ulster Kings"
              },
              {
                "uuid": "fa007",
                "name": "Norse-Irish"
              }
            ],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0001",
                "section": "Lengthy description of the field in the battle\\'s aftermath"
              },
              {
                "uuid": "chprtsum0002",
                "section": "Mac Bais is wandering around the battlefield, looking around in childish (autistic) wonder"
              },
              {
                "uuid": "chprtsum0003",
                "section": "Mac Bais kills for the first time here as a dying man grabs him and hold on to him"
              },
              {
                "uuid": "chprtsum0004",
                "section": "Mac Bais is unbothered by the scene"
              },
              {
                "uuid": "chprtsum0005",
                "section": "Eabha is there, looting the dead by her husband\\'s order"
              },
              {
                "uuid": "chprtsum0006",
                "section": "Eabha notices Mac Bais , they interact, bond, and she takes him with her back home."
              }
            ]
          },
          {
            "uuid": "chprt002",
            "name": "Chapter 1 - Part 2",
            "perspective": {
              "uuid": "sg002",
              "description": "Infant Mac Bais"
            },
            "location": {
              "uuid": "l105",
              "description": "Clontarf"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              }
            ],
            "themes": [
              {
                "uuid": "th001",
                "name": "violence and youth"
              },
              {
                "uuid": "th002",
                "name": "death and life"
              },
              {
                "uuid": "th003",
                "name": "innocence"
              },
              {
                "uuid": "th004",
                "name": "vulnerability"
              },
              {
                "uuid": "th005",
                "name": "love"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0007",
                "section": "get his first person perspective of the above from the moments after the man dies"
              },
              {
                "uuid": "chprtsum0008",
                "section": "after leaving the battlefield he relives his first permanent memory, killing the man and meeting Eabha"
              },
              {
                "uuid": "chprtsum0009",
                "section": "he is completely neutral about the killing, it was a puzzle to solve and he solved it"
              },
              {
                "uuid": "chprtsum0010",
                "section": "but has a new feeling that he hasn\\'t experienced before for Eabha (love)"
              }
            ]
          },
          {
            "uuid": "chprt003",
            "name": "Chapter 1 - Part 3",
            "perspective": {
              "uuid": "sg001",
              "description": "Teenage Eabha"
            },
            "location": {
              "uuid": "l105",
              "description": "Clontarf"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              }
            ],
            "themes": [
              {
                "uuid": "th001",
                "name": "violence and youth"
              },
              {
                "uuid": "th002",
                "name": "death and life"
              },
              {
                "uuid": "th003",
                "name": "innocence"
              },
              {
                "uuid": "th004",
                "name": "vulnerability"
              },
              {
                "uuid": "th006",
                "name": "protective"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0011",
                "section": "get her first person perspective of events of part 1"
              },
              {
                "uuid": "chprtsum0012",
                "section": "she somehow senses Mac Bais and she are tied together forever now"
              },
              {
                "uuid": "chprtsum0009",
                "section": "she is unsure how The Blacksmith will react, she fears beatings for them both"
              },
              {
                "uuid": "chprtsum0010",
                "section": "she thinks about Mac Bais, how he behaves, what she is starting to understand about him, and what the premonition she has about their being bound forever might mean"
              }
            ]
          }
        ]
    },
    {
      "uuid": "cho002",
      "story_event": {
        "uuid": "se002"
      },
      "chapter": {
        "uuid": "chp002",
        "chapter_num": 2
      },
      "summary": "The Blacksmith, waits for his wife\\'s return. She returns with Mac Bais and he accepts him into his home (Outskirts of Dublin, Ireland, year 1014).",
        "parts": [
          {
            "uuid": "chprt004",
            "name": "Chapter 2 - Part 1",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l101",
              "description": "The Forge/Blacksmith\\'s House"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th004",
                "name": "vulnerability"
              },
              {
                "uuid": "th007",
                "name": "resentment"
              },
              {
                "uuid": "th008",
                "name": "acceptance"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0013",
                "section": "The Blacksmith is working alone at the forge, which is also their home"
              },
              {
                "uuid": "chprtsum0014",
                "section": "Descriptive content: the experiences and emotions of being a blacksmith, the sounds, smells, temperatures, injuries, dangers, hardness, satisfaction, boredom, banality of the work"
              },
              {
                "uuid": "chprtsum0015",
                "section": "Waiting for Eabha\\'s return, he had sent her to the aftermath of the battle to loot for anything valuable that he could smith into jewelry to sell."
              },
              {
                "uuid": "chprtsum0016",
                "section": "We get an insight into his mind, his bitter thoughts and emotions, hints at why he feels this way but don\\'t go into detail, he is filled with excuses for not living the life he wants, blaming others. He hates everyone and everything, and feels he has good reason to."
              },
              {
                "uuid": "chprtsum0017",
                "section": "currently working on making farm tools - he hates the banality of this work."
              },
              {
                "uuid": "chprtsum0018",
                "section": "Embittered by Éabha\\'s inability to bear children, he spent everything he had on buying her from the slavers. There is no evidence the fertility problem does not lie with him."
              },
              {
                "uuid": "chprtsum0019",
                "section": "looking forward to the enjoyment of receiving the valuables Éabha\\' has discovered, or the satisfaction of beating her for not finding anything worth the time she spent looking."
              },
              {
                "uuid": "chprtsum0020",
                "section": "this part ends with The Blacksmith noticing the silhouette of two children emerging over the horizon"
              }
            ]
          },
          {
            "uuid": "chprt005",
            "name": "Chapter 2 - Part 2",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l101",
              "description": "The Forge/Blacksmith\\'s House"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th004",
                "name": "vulnerability"
              },
              {
                "uuid": "th008",
                "name": "acceptance"
              },
              {
                "uuid": "th010",
                "name": "family"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0021",
                "section": "Mac Bais and Eabha approach The Forge"
              },
              {
                "uuid": "chprtsum0022",
                "section": "Eabha has been worrying about The Blacksmith\\'s reaction"
              },
              {
                "uuid": "chprtsum0023",
                "section": "Eabha is relieved that he is happy with her for the gift of this boy child she has brought back"
              },
              {
                "uuid": "chprtsum0024",
                "section": "he vows to be a more gentle and tender husband, and good father"
              },
              {
                "uuid": "chprtsum0025",
                "section": "he is playful with Mac Bais and offers to make them food"
              },
              {
                "uuid": "chprtsum0026",
                "section": "the scene as they enter the forge, their home, is gentle, comfortable, serene"
              }
            ]
          },
          {
            "uuid": "chprt006",
            "name": "Chapter 2 - Part 3",
            "perspective": {
              "uuid": "sg001",
              "description": "Teenage Eabha\\'s 1st Person Narrative"
            },
            "location": {
              "uuid": "l101",
              "description": "The Forge/Blacksmith\\'s House"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th004",
                "name": "vulnerability"
              },
              {
                "uuid": "th011",
                "name": "repressed anger"
              },
              {
                "uuid": "th012",
                "name": "hope"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0027",
                "section": "Eabha is relieved they haven\\'t been beaten."
              },
              {
                "uuid": "chprtsum0028",
                "section": "In the mental and emotional space that this relief has opened up in her, her mind wanders"
              },
              {
                "uuid": "chprtsum0029",
                "section": "and lands on a repressed anger, fury, desire for revenge against The Blacksmith"
              },
              {
                "uuid": "chprtsum0030",
                "section": "she locks it away, she knows where it is, and knows that some day, with Mac Bais, she will be able to release it"
              }
            ]
          }
        ]
      
    },
    {
      "uuid": "cho003",
      "story_event": {
        "uuid": "se003"
      },
      "chapter": {
        "uuid": "chp003",
        "chapter_num": 3
      },
      "summary": "As the months pass, The Blacksmith realizes Mac Bais is \"useless\" - he increasingly returns to being abusive. (Outskirts of Dublin, Ireland, year 1014).",

        "parts": [
          {
            "uuid": "chprt007",
            "name": "Chapter 3 - Part 1",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l100",
              "location": "The Village"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th007",
                "name": "change"
              },
              {
                "uuid": "th013",
                "name": "transition"
              },
              {
                "uuid": "th009",
                "name": "abuse"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0025",
                "section": "Leaving the new found serenity of The Forge, begin an evocative description of The Blacksmith\\'s Village and its inhabitants as it passes from Spring into Fall"
              },
              {
                "uuid": "chprtsum0026",
                "section": "Return to The Forge approaching winter, it is a much less serene scene than The Forge we left in Spring"
              },
              {
                "uuid": "chprtsum0027",
                "section": "Mac Bais finds Eabha angry and tearful, but not crying, washing clothes in the brook that passes through their land."
              }
            ]
          },
          {
            "uuid": "chprt008",
            "name": "Chapter 3 - Part 2",
            "perspective": {
              "uuid": "sg001",
              "description": "Eabha"
            },
            "location": {
              "uuid": "l101",
              "description": "The Blacksmith\\'s Village"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th015",
                "name": "realization"
              },
              {
                "uuid": "th014",
                "name": "jealousy"
              },
              {
                "uuid": "th009",
                "name": "abuse"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0028",
                "section": "It is close to Winter, the blacksmith\\'s initial warmth has faded."
              },
              {
                "uuid": "chprtsum0029",
                "section": "It is clear now that the boy is in some way different (autistic), he will never make a good husband, bring a good dowry, work the blacksmith\\'s shop, or be useful in any way to The Blacksmith."
              },
              {
                "uuid": "chprtsum0030",
                "section": "The Blacksmith hasn\\'t said any of this, but Eabha has read it in him."
              },
              {
                "uuid": "chprtsum0031",
                "section": "He grows jealous of the bond between Eabha and Mac Bais, and increasingly takes his anger out on Éabha."
              }
            ]
          },
          {
            "uuid": "chprt009",
            "name": "Chapter 3 - Part 3",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l101",
              "description": "The Blacksmith\\'s Village"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th006",
                "name": "protectiveness"
              },
              {
                "uuid": "th013",
                "name": "adaptation"
              },
              {
                "uuid": "th009",
                "name": "abuse"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0032",
                "section": "Mac Bais, initially oblivious of the increasing abuse, eventually senses Éabha\\'s distress."
              },
              {
                "uuid": "chprtsum0033",
                "section": "He starts to notice feelings of protectiveness over her."
              },
              {
                "uuid": "chprtsum0034",
                "section": "Mac Bais deduces that Eabha is abused because there is something wrong with him that makes The Blacksmith angry."
              },
              {
                "uuid": "chprtsum0035",
                "section": "Mac Bais attempts to mask those parts of himself."
              }
            ]
          },
          {
            "uuid": "chprt010",
            "name": "Chapter 3 - Part 4",
            "perspective": {
              "uuid": "sg002",
              "name": "Infant Mac Bais"
            },
            "location": {
              "uuid": "l101",
              "location": "The Forge/Blacksmith\\'s House"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              }
            ],
            "themes": [
              {
                "uuid": "th006",
                "name": "protectiveness"
              },
              {
                "uuid": "th011",
                "name": "repressed anger"
              },
              {
                "uuid": "th009",
                "name": "abuse"
              },
              {
                "uuid": "th015",
                "name": "realization"
              },
              {
                "uuid": "th017",
                "name": "revenge"
              },
              {
                "uuid": "th005",
                "name": "love"
              },
              {
                "uuid": "th001",
                "name": "violence and youth"
              }
            ],
            "factions": [],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0036",
                "section": "After a few months of masking the traits in him that trouble The Blacksmith, he finds Eabha angry and tearful, but not crying, washing clothes in the brook that passes through their land."
              },
              {
                "uuid": "chprtsum0037",
                "section": "she has an injury from The Blacksmith"
              },
              {
                "uuid": "chprtsum0038",
                "section": "Mac Bais finds a new feeling in him he has never felt before, destructive fury"
              }
            ]
          }
        ]
    },
    # {
    #   "uuid": "cho004",
    #   "story_event": {
    #     "uuid": "se000"
    #   },
    #   "chapter": {
    #     "uuid": "chp004",
    #     "chapter_num": 4
    #   },
    #   "summary": "Eabha\\'s Dream",
    #   "parts": [
    #       {"string":"This is a differnt kind of chapter\n\nEabha has a recurring dream, it comes up every now and then in the story. I have to still outline it.\n\nIt is premenmotory and terrible and becomes less vauge as the book progresses.\n\nBut at this stage it is not vivid, it is vague, difficult to discern meaning and filled with terror and fear and uncertainty"}
    #       ]
    # },
    {
      "uuid": "cho005",
      "story_event": {
        "uuid": "se004"
      },
      "chapter": {
        "uuid": "chp005",
        "chapter_num": 5
      },
      "summary": " Time passes, the town goes through events, harvests, church growing in power, Viking raids means more work for The Blacksmith, means more importance, money power and influence for him",

        "parts": [
          {
            "uuid": "chprt011",
            "name": "Chapter 5",
            "perspective": {
              "uuid": "sg000",
              "description": "The Narrator"
            },
            "location": {
              "uuid": "l100",
              "location": "The Village"
            },
            "characters": [
              {
                "uuid": "001",
                "name": "Eabha"
              },
              {
                "uuid": "002",
                "name": "Mac Bais"
              },
              {
                "uuid": "003",
                "name": "The Blacksmith"
              }
            ],
            "themes": [
              {
                "uuid": "th007",
                "name": "change"
              },
              {
                "uuid": "th013",
                "name": "transition"
              },
              {
                "uuid": "th009",
                "name": "abuse"
              }
            ],
            "factions": [
              {
                "uuid": "fa001",
                "name": "Vikings"
              },
              {
                "uuid": "fa002",
                "name": "Christian Zealots"
              },
              {
                "uuid": "fa007",
                "name": "Norse-Irish"
              }
            ],
            "chapter_part_summary": [
              {
                "uuid": "chprtsum0039",
                "section": "increasing consolidation of power of the Catholic Church"
              },
              {
                "uuid": "chprtsum0040",
                "section": "gossip about Eabha and Mac Bais grows in the village"
              },
              {
                "uuid": "chprtsum0041",
                "section": "some good and bad harvest years"
              },
              {
                "uuid": "chprtsum0042",
                "section": "A number of viking raids on the local monastery, they build a round tower for protection"
              },
              {
                "uuid": "chprtsum0043",
                "section": "lots of work for the blacksmith due to the raids, he welcomes hearing of them"
              },
              {
                "uuid": "chprtsum0044",
                "section": "The Blacksmith\\'s influence in The Village is greatly increased, especially with the local clergy."
              },
              {
                "uuid": "chprtsum0045",
                "section": "He is important, but people don\\'t really like him"
              }
            ]
          }
        ]
      
    }
  ],
  "story_rules": [
    "There is no proof or certainty that anything mythological happens in the story, but the world through their eyes is steeped in the mythology of medieval Ireland, and the readers are never left completely sure whether or not something mystical could be happening.",
    "Mac Bais\\' autistic \"abilities\" aren\\'t fully understood by characters, narrators or readers, autism is NEVER mentioned. He is frequently interpretable as connected to the ancient magic of Ireland (and Newfoundland Native Americans) by secondary characters or readers.",
    "Éabha\\'s abilities to manipulate, scheme and make sense of the desires and motivations of others is also frequently interpreted as a mythological power",
    "Most of the time the story is told from a neutral 3rd person perspective that focusses on Éabha and Mac Báis",
    "Occasionally certain chapters or parts of chapters are in first person, present tense, stream of consciousness for one of the main characters",
    "Less occasionally, (every 3 to 7 chapters) The Narrator goes to a 3rd person perspective of another character that Éabha and Mac Báis have encountered or will encounter. These chapters can be set before or after the time they meet our protagonists.",
    "Some of these chapters, or parts of chapters, are in the form of songs or poems or stories or mythologies told by the bards or druids or storytellers of Ireland. Sometimes these secondary character versions of the story are told hundreds of years later, with a framing device of some kind"
  ],
  "book_name": "Living and The Son of Death",
  "author": "Sean M Ryan",
  "genres": [
    "hostorical fiction",
    "magical realism"
  ],
  "inspirations": [
    ""
  ],
  "back_of_book_blurb": "",
  "summaries": [
    {
      "market": "fantasy",
      "summary": "BLARBB"
    }
  ],
  "lit_style_guides": [
    {
      "name": "The Narrator\\'s Style Guide",
      "character": {
        "uuid": "000",
        "name": "The Narrator"
      },
      "uuid": "sg000",
      "inspirations": [
        "Cormac McCarthy",
        "William Faulkner",
        "William S Burroughs",
        "Charles Bukowski",
        "Nick Cave",
        "Tom Waits"
      ],
      "traits": [
        "omnipotent",
        "ethically neutral",
        "fascinated with darkness",
        "suggestive of hidden mythological and/or Lovecraftian forces",
        "could perhaps themselves be a Lovecraftian monster",
        "May also be the author of the Old Testament",
        "a hint that they may have more power over the story"
      ],
      "avoid": [
        "optimism",
        "hopefulness",
        "faith/presumptions in the good hearts of people",
        "redemption",
        "reconciliation",
        "tendency to peaceful or positive or happy outcomes"
      ],
      "style_guide": [
        "Use sparse punctuation: Minimize the use of punctuation, particularly commas and quotation marks. Allow the sentences to flow together, making the continuity and intensity of the prose dreamlike (more often, nightmare like). Favor run-on sentences that bring a relentless pace to the prose with very few commas. but also employ occasional sentence fragments.",
        "Write long, complex sentences: Construct sentences with multiple clauses and ideas, letting them run on and weave together. This will add to the depth and richness of the prose.",
        "Use descriptive language: Employ vivid, evocative language to create a strong sense of atmosphere and setting. Focus on details that convey the nightmarishness, harshness, beauty, or complexity of the world and its inhabitants. Intensify the language to create a richer atmosphere and stronger sense of setting, particularly when describing the environment.",
        "Sparing use of pronouns and names: Rely on context and the reader\\'s understanding to convey who is speaking or being referred to.",
        "Maintain a neutral, detached tone, dispassionate and objective, allow the reader to draw their own conclusions about the characters\\' emotions, motivations, and morality.",
        "Convey emotions and thoughts indirectly: Show characters\\' feelings and thoughts through their actions, body language, or the environment, rather than stating them outright.",
        "Create an atmosphere of tension and uncertainty: Allow the reader to sense the undercurrents of emotions, suspicions, and potential conflict between characters, without explicitly stating them.",
        "Explore themes of brutality, cruelty, and struggle: Delve into the bleaker aspects of human nature, as well as the challenges and hardships faced by the characters",
        "Use poetic prose: Write with a sense of poetry, incorporating rhythm, imagery, and symbolism to elevate the prose and create a more immersive reading experience.",
        "Trust the reader\\'s intelligence: Avoid over-explaining or spelling out every detail. Allow the reader to fill in the gaps and make connections based on the information provided in the text.",
        "Utilize more archaic, ancient, biblical language, adding a sense of timelessness and gravitas to the narrative.",
        "Incorporate more philosophical or existential musings into the narrative, weave larger themes and questions into the narrative."
      ],
      "compressed": [
        "Use sparse punctuation, flow sentences together, favor run-ons and occasional fragments, intensify language to create atmosphere",
        "Write long, complex sentences to add depth and richness to prose",
        "Use vivid, evocative language to create a strong sense of atmosphere and setting",
        "Sparingly use pronouns and names, rely on context",
        "Maintain a neutral, detached tone, convey emotions and thoughts indirectly",
        "Create an atmosphere of tension and uncertainty, explore themes of brutality and struggle",
        "Use poetic prose with rhythm, imagery, and symbolism to create immersive experience",
        "Trust reader\\'s intelligence, avoid over-explaining",
        "Use archaic, biblical language for timelessness and gravitas",
        "Incorporate philosophical and existential musings, weave larger themes into narrative"
      ],
      "writing_samples": [
        "In the depths of a moonless night, there came a stillness, a quiet so profound it seemed as if the world held its breath. The Blacksmith, the fire dimmed in his forge, stepped out into the darkness, carrying on him the a lifetime of bitterness. He stood there, an empty silhouette amidst the vast expanse of the dark and indifferent cosmos. The glistening stars ignoring him cold, their distance and their divinity a sardonic rebuke to the tiny nothing of this one man\\'s soul.",
        "Through the barren landscape, a storm approached, a harbinger of destruction, of cataclysm, sweeping away all that dared to defy its inexorable march. The wind tore at the earth, uprooting and scattering the dry dust, as if the land itself sought to escape its own desolation. The two, wrapped in tattered cloaks, forged ahead, their faces stung by biting sand, eyes squinted against the onslaught. The child held close, a fragile being in a merciless world, against the storm that sought to asunder each.",
        "Shadows stretched long and thin in the dim light of the dying day, like fingers of some ancient god grasping out for the earth as the sun\\'s last ember faded beneath the horizon. The Blacksmith and Éabha, their bodies weary and spirits worn, found a river, waters black as ink, coursing through the desolation. The murmur of it whispered tales of sorrow and hope, of life that clung to the edge of precipice."
      ]
    },
    {
      "name": "Teenage Eabha\\'s 1st Person Narrative Style Guide",
      "character": {
        "uuid": "001",
        "name": "Eabha",
        "version": 1
      },
      "uuid": "sg001",
      "inspirations": [
        "Voice over narration in the films of Terence Malick",
        "Ann Holm\\'s \"I am David\""
      ],
      "traits": [
        "stream of consciousness",
        "strong sense of morals",
        "very aware of the story they are in",
        "she sees the power of relationships with others"
      ],
      "avoid": [
        "description of the world",
        "thoughts about any other than the narrative of past/present/future",
        "abstract thinking"
      ],
      "style_guide": [
        "When in 1st person narrative for Eabha, focus on her understanding of the story going on around her. Where it has been, where it is and where it could go. Her deep understanding of this makes her almost clairvoyant about what is about to happen and how to deal with it.",
        "Similar style of writing as the voice over narration used in the films of Terence Malick, especially The New World and The Tree of Life",
        "Similar style of writing that William Faulkner used for the Quentin chapter of \"The Sound and the Fury\" - but not so miserable, powerless, defeated, self-absorbed",
        "Focus more on her connection to others, her ability to read people and to manipulate them, her self-awareness of her strengths and weaknesses, and the strengths and weaknesses of the people around her, her sense of past present and future and how they connect to each other, what people can offer her and what she can offer to people."
      ],
      "compressed": [],
      "writing_samples": []
    },
    {
      "name": "Infant Mac Bais\\' 1st Person Narrative Style Guide",
      "character": {
        "uuid": "002",
        "name": "Mac Bais",
        "version": 1
      },
      "uuid": "sg002",
      "inspirations": [
        "Imagist Poetry",
        "The Benjy chapter of \"The Sound and the Fury\" by William Faulkner",
        "Finnegans Wake"
      ],
      "traits": [
        "stream of consciousness",
        "ethically neutral",
        "fascinated by novel sensory experiences",
        "mostly unaware of the story happenning around him",
        "curious",
        "hyperfocusses on odd sensations",
        "literary/poetic descriptions of phenomoenological experience"
      ],
      "avoid": [
        "optimism",
        "hopefulness",
        "faith/presumptions in the good hearts of people",
        "redemption",
        "reconciliation",
        "tendency to peaceful or positive or happy outcomes"
      ],
      "style_guide": [
        "When in 1st person narrative for Infant Mac Bais, focus more on phenomenological sensory experience",
        "Thoughts, memories and experiences usually make sense to him but may be a jumble to readers. They make less sense to him when Eabha is not around, or when he is stressed",
        "Similar style of writing to the Benjy chapter of \"The Sound and the Fury\" by William Faulkner - but less \\'disabled\\' and more self aware of his story, powers and weaknesses",
        "His attention is drawn more to the sensory experiences of his scenes, he is aware that other things are going on, but would pay more attention to the feeling of a the grass, or the warmth of the sun on his skin, rather than the awful aftermath of battle around him"
      ],
      "compressed": [
        "In 1st person narrative for Infant Mac Bais, focus on sensory experience",
        "Thoughts and memories make sense to him but may be confusing for readers. He\\'s less clear-headed without Eabha or under stress",
        "Write in style of Benjy chapter in \"The Sound and the Fury\" by William Faulkner, but more self-aware and less \"disabled\"",
        "Pay more attention to sensory experiences, like feeling the grass or sun on skin."
      ],
      "writing_samples": []
    }
  ]
}
    
def get_instance_if_exists(puuid, model):
    found_instance = -1
    try:
        found_instance = model.objects.filter(puuid=puuid)
        pprint(found_instance)
    except:
        print(f"{puuid} not found")
        
    return found_instance

def generate_instance(target_model, puuid, **kwargs):
    test_appendage = '_tst'
    puuid = f"{puuid}{test_appendage}"
    instance = target_model.objects.create(**kwargs)
    instance.puuid = puuid
    print(f"{instance.__str__} created")
    return instance   
    
def add_data_to_instance(instance, fieldName, data):
    instance.get_field(fieldName).set(data)
    pprint(instance)

def push_to_db(instance):
    with transaction.atomic():
        instance.save(using='default')
          
class Command(BaseCommand):
  help = "fiugure it out man"
  
  def handle(self, *args, **options):
      main()

def main():
    global content
    
    book_name = content['book_name']
    book_instance = generate_instance(Book, book_name, name=book_name)
    pprint(book_instance)
    
    chapters =  content["chapters"]
    for chapter in chapters:
      # pprint(chapter)
      instance = generate_instance(Chapter, chapter["uuid"], chapter_num=chapter["chapter_num"], book_id=book_instance.id)
      
    story_rules_arr = content["story_rules"]
        
    genres =  content["genres"]
    for genre in genres:
      pprint(genre)
      instance = generate_instance(Genre, genre, book_id=book_instance.id, name=genre)
    
    chapter_parts =  content["chapter_parts"]
    for chapter_part in chapter_parts:
      pprint(chapter_part)
      instance = generate_instance(ChapterPart, chapter_part["uuid"], part_num=chapter_part["part"])
      pprint(instance)
      
    chapter_part_summary_items = content["chapter_part_summary"]
    for item in chapter_part_summary_items:
        uuid = item['uuid']
        section = item['section']
              
    themes =  content["themes"]
    for theme in themes:
        uuid = theme['uuid']
        name = theme['name']
    
    factions =  content["factions"]
    for faction in factions:
        uuid = faction['uuid']
        name = faction['name']
    
    locations =  content["locations"]
    for location in locations:
        uuid = location['uuid']
        name = location["location"]
    
    bg_events_arr = content["background_events"]
    for bg_event in bg_events_arr:
        uuid = bg_event['uuid']
        event_str = bg_event["event"]
        year_from = bg_event["year"] #this could be a float or an obj   
        
    setting = content["setting"]
    general_setting = setting["general_setting"]
    
    deeper_bg_research_topics = content["deeper_background_research"]

    for bg_research_topic in deeper_bg_research_topics:
        uuid = bg_research_topic['uuid']
        topic_str = bg_research_topic["topic"]
        notes = bg_research_topic["notes"]
        for n in notes:
            note = n
    
    character_related_setting_infos = content["character_related_setting_info"]
    for char_stt_infor in character_related_setting_infos:
        uuid = char_stt_infor['uuid']
        name_str = char_stt_infor["name"]
        character_dict = char_stt_infor["character"]
        char_uuid = character_dict['uuid']
        version = character_dict['version']      
        character_arr = char_stt_infor["rights"]
        appearance_modifiers_dict = char_stt_infor["appearance_modifiers"]
        clothing_arr = appearance_modifiers_dict['clothing']
        hair_head_options_arr = appearance_modifiers_dict['hair_head_options']
        perfume = appearance_modifiers_dict['perfume']
        makeup = appearance_modifiers_dict['makeup']
        shaving = appearance_modifiers_dict['shaving']
        hugiene = appearance_modifiers_dict['washing_schedule']
        attitudes_arr = char_stt_infor["attitudes"]       
        leisure_arr = char_stt_infor["leisure"]
        food_arr = char_stt_infor["food"]
        work_arr = char_stt_infor["work"]
        social_life_arr = char_stt_infor["social_life"]
        
    main_characters_arr =  content["main_characters"]
    for main_character in main_characters_arr:
        uuid = main_character['uuid']
        name = main_character["name"]
        age_at_start = main_character["age_at_start"]
        gender = main_character["gender"]
        origin = main_character["origin"]
        representative_of_arr = main_character["representative_of"]
        for n in notes:
            note = n
        
        permanent_characteristics_arr = main_character["permanent_characteristics"]
        for n in notes:
            note = n
        
        character_versions_arr = main_character["character_versions"]
        for n in notes:
            note = n
    
    main_characters_relationship_str =  content["main_characters_relationship"]
    
    secondary_characters_arr = content["secondary_characters"]
    for char in secondary_characters_arr:
        uuid = char['uuid']
        name = char["name"]
        age_at_start = char["age_at_start"]
        strengths_arr = char["strengths"]
        for n in notes:
            note = n
        
        weaknesses_arr = char["weaknesses"]
        for n in notes:
            note = n
        
        representative_of_arr = char["representative_of"]
        for n in notes:
            note = n
        
        other_aspects_arr = char["other_aspects"]
        for n in notes:
            note = n
        
        often_perceived_as_arr = char["often_perceived_as"]
        for n in notes:
            note = n
        
        drives = char["drives"]
        for n in notes:
            note = n
        
        fears = char["fears"]
        for n in notes:
            note = n
        
        relationships = char["relationships"]
        for n in notes:
            note = n
    
    plot_events =  content["story_events"]
    for plot_event in plot_events:
        uuid = plot_event['uuid']
        themes_arr = plot_event['themes']       
        location_uuid = plot_event['location_uuid']
        description = plot_event['description']
        # year = plot_event['year']
        character_uuids = plot_event['character_uuids']
        for n in notes:
            note = n   
        
        
    chapter_outlines =  content["chapter_outlines"]
    for ch in chapter_outlines:
        uuid = ch['uuid']
        story_event_uuid = ch['story_event']
        chapter_uuid = ch['chapter']['uuid']
        summary = ch['summary']
        parts = ch['parts']
        for n in notes:
            note = n
    
    lit_style_guides =  content["lit_style_guides"]
    for sg in lit_style_guides:
        name = sg['name']
        character_uuid = sg['character']['uuid']
        inspirations = sg['inspirations']
        for n in notes:
            note = n
        
        traits = sg['traits']
        for n in notes:
            note = n
        
        avoid = sg['avoid']
        for n in notes:
            note = n
        
        style_guides = sg['style_guide']
        for n in notes:
            note = n
        
        compressed_sg = sg['compressed']
        writing_samples = sg['writing_samples']
        for n in notes:
            note = n  



if __name__ == "__main__":
    main()

