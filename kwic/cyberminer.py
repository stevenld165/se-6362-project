from sqlalchemy import Select, and_, desc, exists, not_, or_, select
from sqlalchemy.orm import Session

from database import KwicEntry, Website, engine
from kwic.kwic import Kwic

import random


class Cyberminer:
    def __init__(self):
        self.kwic = Kwic()
    # add website
    def add_website(self, url: str, desc: str):
        shifts = self.kwic.addWebsite(desc)
        with Session(engine) as session:
            website = Website(
                url = url,
                desc = desc,
                accesses = 0,
                sponsorMoney = 0
            )

            session.add(website)
            session.flush()

            for shift in shifts:
                kwic_entry = KwicEntry(
                    website_id = website.id,
                    first_word = shift["first_word"],
                    full_circular_shift = shift["full_circular_shift"]
                )

                session.add(kwic_entry)
            
            session.commit()

        print("added")
    # remove website
    def remove_website(self, website_id: int):
        print("removed")
    def search(self, keywords, mode, sortOrder):
        # assume or mode first
        with Session(engine) as session:
            stmt = None

            match mode:
                case "OR":
                    stmt = select(Website).join(Website.kwic_entries).where(
                        or_(*[KwicEntry.first_word.like(keyword + "%") for keyword in keywords])
                    ).distinct()
                case "AND":
                    stmt = select(Website).join(Website.kwic_entries)

                    for keyword in keywords:
                        stmt = stmt.where(
                            Website.kwic_entries.any(KwicEntry.first_word.like(keyword + "%"))
                        )

                    stmt = stmt.distinct()
                case "NOT":
                    stmt = select(Website).join(Website.kwic_entries).where(
                        or_(*[~Website.kwic_entries.any(KwicEntry.first_word.like(keyword + "%")) for keyword in keywords])
                    ).distinct()
                case _:
                    stmt = select(Website).join(Website.kwic_entries).where(
                        or_(*[KwicEntry.first_word.like(keyword + "%") for keyword in keywords])
                    ).distinct()
            

            match sortOrder:
                case "url":
                    stmt = stmt.order_by(Website.url)
                case "accesses":
                    stmt = stmt.order_by(desc(Website.accesses))
                case "sponsorMoney":
                    stmt = stmt.order_by(desc(Website.sponsorMoney))
                case _:
                    stmt = stmt.order_by(Website.url)

            return session.execute(stmt).all()
        print("failed")
    # def searchSlow(self, keywords):
    #     with Session(engine) as session:
    #         stmt = select(Website).where(
    #                     or_(*[Website.desc.like("%" + keyword + "%") for keyword in keywords])
    #                 ).distinct().order_by(Website.url)
    #         return session.execute(stmt).all()
    def visit(self, website_id):
        # add code for when you visit a website to increment the thing
        return
    def addSponsorPayment(self, website_id):
        # add code for adding to sponsor payment
        return    
    

    

    