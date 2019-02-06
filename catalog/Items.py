#!/user/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Dbcreation import Category, Base, MenuItem, User

engine = create_engine('sqlite:///products.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
user1 = User(name="GopiBarma", email="gopibarma44@gmail.com",
             picture="https://o.aolcdn.com/images/dims3/GLOB/"
             "legacy_thumbnail/1200x630/format/jpg/quality/85/"
             "http%3A%2F%2Fi.huffpost.com%2Fgen%2F5334782"
             "%2Fimages%2Fn-TWIN-BABY-628x314.jpg")
session.add(user1)
session.commit()

# adding product1
product1 = Category(user_id=1, name="Mobiles")
session.add(product1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Honor 7A",
                     description="Capture the best moments of your life with"
                     "the 13MP + 2MP ultra sharp dual-lens camera.",
                     price="Rs 9000", course="smartPhone",
                     img="/static/images/lenovop2.jpg",
                     product_id=1, product=product1)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Samsung",
                     description="Galaxy A8 Star features an ergonomic,"
                     "near bezel-less design that minimizes distraction.",
                     price="Rs 9000", course="smartPhone",
                     img="/static/images/samsung.jpeg",
                     product_id=1, product=product1)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Realmi",
                     description="A quick face scan or one simple touch on the"
                     "Fingerprint Sensor and the Realme lays out.",
                     price="Rs 9000", course="smartPhone",
                     img="/static/images/realme-2.jpeg",
                     product_id=1, product=product1)
session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(user_id=1, name="Redmi Note 6 Pro",
                     description="A 20 MP + 2 MP dual front camera,"
                     "a long-lasting battery and 15.9 cm (6.26-inch) "
                     "screen - there is so much to love about the"
                     "Redmi Note 6 Pro.", price="Rs 7000",
                     course="smartPhone",
                     img="/static/images/mi.jpeg",
                     product_id=1, product=product1)
session.add(menuItem4)
session.commit()

# adding product2
product2 = Category(user_id=1, name="Laptops")
session.add(product2)
session.commit()

menuItem1 = MenuItem(user_id=1, name="LenovoIdeapad320",
                     description="Looks, performance, and durability - the"
                     "IdeaPad 320 has it all and more.",
                     price="Rs 45000", course="Keypad",
                     img="/static/images/lenovo-ip-320.jpeg",
                     product_id=2, product=product2)
session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(user_id=1, name="Dell Inspiron 15 3000 Series",
                     description="Looks, performance, and durability - the"
                     "IdeaPad 320 has it all and more.",
                     price="Rs 40000", course="smartPhone",
                     img="/static/images/dell.jpg",
                     product_id=2, product=product2)
session.add(menuItem2)
session.commit()


menuItem3 = MenuItem(user_id=1, name="Apple MacBook Air",
                     description="The speed and smooth performance of this"
                     "MacBook Air is certain to impress.",
                     price="Rs 40000", course="smartPhone",
                     img="/static/images/apple-na-thin.jpeg",
                     product_id=2, product=product2)
session.add(menuItem3)
session.commit()

product3 = Category(user_id=1, name="Tv's")
session.add(product3)
session.commit()

menuItem1 = MenuItem(user_id=1, name="LG Smart 80cm",
                     description="This sleek LG Smart TV lends itself as the"
                     "perfect one-stop shop for all things entertainment.Other"
                     "than checking out the whats of regular TV channels",
                     price="Rs 20000", course="SmartTv",
                     img="/static/images/lg-Tv.jpeg",
                     product_id=3, product=product3)
session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(user_id=1, name="Mi LED Smart TV 4A 80 cm",
                     description="This sleek LG Smart TV lends itself as the"
                     "perfect one-stop shop for all things entertainment.Other"
                     "than checking out the whats of regular TV channels",
                     price="Rs 12000",
                     course="SmartTv",
                     img="/static/images/mi1.jpeg",
                     product_id=3, product=product3)
session.add(menuItem2)
session.commit()


menuItem3 = MenuItem(user_id=1, name="Samsung 80cm (32 inch)",
                     description="Watch movies, sports, series and much more"
                     "with vivid and lifelike details on the Samsung Series HD"
                     "Ready LED TV.",
                     price="Rs 15000",
                     course="SmartTv",
                     img="/static/images/samsung-32.jpeg",
                     product_id=3, product=product3)
session.add(menuItem3)
session.commit()

# adding product3

print("added menu items!")
