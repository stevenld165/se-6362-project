from sqlalchemy import Select, and_, desc, exists, not_, or_, select
from sqlalchemy.orm import Session

from database import KwicEntry, Website, db
from kwic.kwic import Kwic

import random


class Cyberminer:
    def __init__(self):
        self.kwic = Kwic()
    # add website
    def add_website(self, url: str, desc: str):
        shifts = self.kwic.addWebsite(desc)

        website = Website(
            url = url,
            desc = desc,
            accesses = 0,
            sponsorMoney = 0
        )

        db.session.add(website)
        db.session.flush()

        for shift in shifts:
            kwic_entry = KwicEntry(
                website_id = website.id,
                first_word = shift["first_word"],
                full_circular_shift = shift["full_circular_shift"]
            )

            db.session.add(kwic_entry)
        
        db.session.commit()

        print("added")
    # remove website
    def remove_website(self, website_id: int):
        website = db.session.get(Website, website_id)
        db.session.delete(website)
        db.session.commit

        print(f"Deleted: {website}")
    def search(self, keywords, mode, sort_order, page_num=1, items_per_page=5):
        # assume or mode first
        print("searching!")

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
        

        match sort_order:
            case "url":
                stmt = stmt.order_by(Website.url)
            case "accesses":
                stmt = stmt.order_by(desc(Website.accesses), Website.url)
            case "sponsorMoney":
                stmt = stmt.order_by(desc(Website.sponsorMoney), Website.url)
            case _:
                stmt = stmt.order_by(Website.url)

        offset = (page_num - 1) * items_per_page
        stmt = stmt.limit(items_per_page).offset(offset)

        result = db.session.execute(stmt).all()

        print(result)

        return result
        print("failed")
    # def searchSlow(self, keywords):
    #     with Session(engine) as session:
    #         stmt = select(Website).where(
    #                     or_(*[Website.desc.like("%" + keyword + "%") for keyword in keywords])
    #                 ).distinct().order_by(Website.url)
    #         return session.execute(stmt).all()
    def visit(self, website_id):
        website = db.session.get(Website, website_id)
        website.accesses += 1
        db.session.commit()
        return website.url
    def addSponsorPayment(self, website_id, incrementAmount: float):
        website = db.session.get(Website, website_id)
        website.sponsorMoney += incrementAmount
        db.session.commit()
        return    
    def seed(self):
        self.add_website("https://www.wikipedia.com/", "Wikipedia is an extensive online encyclopedia curated and created by the work of a massive group of contributers.")
        self.add_website("https://www.youtube.com", "Youtube is a platform for sharing videos with other users. Currently the most popular video sharing website on the internet.")
        self.add_website("https://www.github.com", "Github is a proprietary developer platform that allows developers to create, store, manage, and share their code.")
        self.add_website("https://store.steampowered.com/", "Steam is the ultimate destination for playing, discussing, and creating games.")
        self.add_website("https://www.figma.com/", "Figma is the leading collaborative design platform for building meaningful products. Design, prototype, and build products faster—while gathering feedback")
        self.add_website("https://www.netflix.com/", "Watch Netflix movies & TV shows online or stream right to your smart TV, game console, PC, Mac, mobile, tablet and more.")
        self.add_website("https://www.reddit.com", "Reddit is a social news aggregation and discussion website where users can submit content, vote on posts, and engage in community discussions across thousands of specialized forums called subreddits.")
        self.add_website("https://www.amazon.com", "Amazon is a global e-commerce platform offering millions of products ranging from electronics to books, with fast shipping and streaming services included.")
        self.add_website("https://www.twitter.com", "Twitter is a microblogging social media platform where users share short messages, news, and updates in real-time with followers worldwide.")
        self.add_website("https://www.facebook.com", "Facebook is a social networking site that allows users to connect with friends and family, share photos and videos, and join interest-based groups.")
        self.add_website("https://www.linkedin.com", "LinkedIn is a professional networking platform where users can build career profiles, connect with colleagues, search for jobs, and share industry insights.")
        self.add_website("https://www.instagram.com", "Instagram is a photo and video sharing social media platform focused on visual content, stories, and creative expression through filters and editing tools.")
        self.add_website("https://www.stackoverflow.com", "Stack Overflow is a question and answer community for programmers to learn, share knowledge, and build their careers through collaborative problem-solving.")
        self.add_website("https://www.medium.com", "Medium is an online publishing platform where writers can share long-form articles, essays, and stories on diverse topics with a global readership.")
        self.add_website("https://www.twitch.tv", "Twitch is a live streaming platform primarily focused on video game streaming, esports competitions, and creative content broadcasts.")
        self.add_website("https://www.spotify.com", "Spotify is a digital music streaming service providing access to millions of songs, podcasts, and playlists from artists around the world.")
        self.add_website("https://www.dropbox.com", "Dropbox is a cloud storage service that lets users store files online, sync them across devices, and share them with others securely.")
        self.add_website("https://www.slack.com", "Slack is a business communication platform offering organized channels, direct messaging, and integration with productivity tools for team collaboration.")
        self.add_website("https://www.discord.com", "Discord is a voice, video, and text communication platform designed for creating communities and connecting gamers, students, and interest groups.")
        self.add_website("https://www.trello.com", "Trello is a visual project management tool using boards, lists, and cards to help teams organize tasks and collaborate on projects.")
        self.add_website("https://www.notion.so", "Notion is an all-in-one workspace combining notes, databases, wikis, and project management tools for personal and team productivity.")
        self.add_website("https://www.canva.com", "Canva is a graphic design platform offering drag-and-drop tools and templates for creating social media graphics, presentations, and marketing materials.")
        self.add_website("https://www.airbnb.com", "Airbnb is an online marketplace connecting travelers with hosts offering unique accommodations and experiences in destinations worldwide.")
        self.add_website("https://www.booking.com", "Booking.com is a travel fare aggregator and metasearch engine for lodging reservations, offering hotels, apartments, and vacation rentals globally.")
        self.add_website("https://www.ebay.com", "eBay is an online auction and shopping website where people and businesses buy and sell a wide variety of goods and services worldwide.")
        self.add_website("https://www.etsy.com", "Etsy is an e-commerce platform focused on handmade, vintage items, and craft supplies, connecting independent creators with buyers.")
        self.add_website("https://www.paypal.com", "PayPal is an online payment system enabling secure money transfers, online purchases, and business transactions across borders.")
        self.add_website("https://www.shopify.com", "Shopify is an e-commerce platform allowing businesses to create online stores, manage inventory, and process payments with integrated tools.")
        self.add_website("https://www.wordpress.com", "WordPress is a content management system and website builder used by millions to create blogs, business sites, and online portfolios.")
        self.add_website("https://www.wix.com", "Wix is a website builder offering drag-and-drop tools and templates for creating professional websites without coding knowledge.")
        self.add_website("https://www.squarespace.com", "Squarespace is a website building and hosting platform known for beautiful designer templates and integrated e-commerce features.")
        self.add_website("https://www.zoom.us", "Zoom is a video conferencing platform offering online meetings, webinars, and collaborative workspaces for remote communication.")
        self.add_website("https://www.duolingo.com", "Duolingo is a language learning platform offering gamified lessons in dozens of languages through mobile and web applications.")
        self.add_website("https://www.coursera.org", "Coursera is an online learning platform partnering with universities and organizations to offer courses, certificates, and degrees in various subjects.")
        self.add_website("https://www.udemy.com", "Udemy is an online learning marketplace featuring thousands of courses taught by instructors on topics ranging from programming to photography.")
        self.add_website("https://www.khanacademy.org", "Khan Academy is a non-profit educational platform providing free video lessons and practice exercises in math, science, humanities, and more.")
        self.add_website("https://www.pinterest.com", "Pinterest is a visual discovery platform where users find and save ideas for recipes, home decor, fashion, and creative projects.")
        self.add_website("https://www.tumblr.com", "Tumblr is a microblogging and social networking site allowing users to post multimedia content and follow other users' blogs.")
        self.add_website("https://www.quora.com", "Quora is a question-and-answer platform where users ask questions and receive answers from community members with relevant expertise.")
        self.add_website("https://www.imdb.com", "IMDb is an online database of information related to films, television series, podcasts, and video games, including cast, crew, and reviews.")
        self.add_website("https://www.yelp.com", "Yelp is a local business directory and review site where users can find, review, and recommend restaurants, shops, and services.")
        self.add_website("https://www.tripadvisor.com", "TripAdvisor is a travel platform featuring reviews, photos, and booking options for hotels, restaurants, attractions, and vacation experiences.")
        self.add_website("https://www.weather.com", "Weather.com provides local and national weather forecasts, severe weather alerts, and interactive weather maps and radar.")
        self.add_website("https://www.cnn.com", "CNN is a news website offering breaking news, analysis, and video coverage of national and international events across various topics.")
        self.add_website("https://www.bbc.com", "BBC is a British public service broadcaster providing news, entertainment, educational content, and streaming services worldwide.")
        self.add_website("https://www.nytimes.com", "The New York Times is a prestigious newspaper offering in-depth journalism, opinion pieces, and multimedia content on global news and culture.")
        self.add_website("https://www.theguardian.com", "The Guardian is a British news organization providing independent journalism, opinion, and analysis on current events and cultural topics.")
        self.add_website("https://www.reuters.com", "Reuters is an international news organization providing breaking news, business, financial, and multimedia content from around the world.")
        self.add_website("https://www.wsj.com", "The Wall Street Journal is a business-focused newspaper offering news, analysis, and insights on markets, economy, and corporate affairs.")
        self.add_website("https://www.forbes.com", "Forbes is a business magazine and website featuring content on finance, investing, technology, entrepreneurship, and leadership.")
        self.add_website("https://www.techcrunch.com", "TechCrunch is a technology news website covering startups, venture capital, emerging technologies, and product launches.")
        self.add_website("https://www.wired.com", "Wired is a technology and culture magazine exploring how emerging technologies affect science, business, entertainment, and politics.")
        self.add_website("https://www.theverge.com", "The Verge is a technology news and media network covering the intersection of technology, science, art, and culture.")
        self.add_website("https://www.arstechnica.com", "Ars Technica is a technology news and information website featuring in-depth analysis, reviews, and guides for tech enthusiasts.")
        self.add_website("https://www.engadget.com", "Engadget is a technology news and reviews site covering consumer electronics, gadgets, and the latest innovations in tech.")
        self.add_website("https://www.cnet.com", "CNET is a technology media website providing product reviews, news, how-to guides, and videos on consumer technology.")
        self.add_website("https://www.mashable.com", "Mashable is a digital media website covering technology, digital culture, entertainment, and social media trends.")
        self.add_website("https://www.buzzfeed.com", "BuzzFeed is a digital media company known for viral content, quizzes, news reporting, and entertainment articles.")
        self.add_website("https://www.vox.com", "Vox is an explanatory journalism website that aims to help readers understand complex news stories and current events.")
        self.add_website("https://www.vice.com", "Vice is a digital media and broadcasting company producing news, documentaries, and cultural content for young adults.")
        self.add_website("https://www.soundcloud.com", "SoundCloud is an audio streaming platform allowing musicians and podcasters to upload, share, and discover audio content.")
        self.add_website("https://www.bandcamp.com", "Bandcamp is an online music platform where independent artists can sell their music directly to fans and listeners.")
        self.add_website("https://www.genius.com", "Genius is a lyrics and music knowledge platform featuring song meanings, annotations, and artist insights from contributors.")
        self.add_website("https://www.allrecipes.com", "Allrecipes is a cooking website featuring user-submitted recipes, reviews, photos, and meal planning tools for home cooks.")
        self.add_website("https://www.foodnetwork.com", "Food Network is a culinary entertainment website offering recipes, cooking videos, chef bios, and food-related shows.")
        self.add_website("https://www.seriouseats.com", "Serious Eats is a food and cooking website providing tested recipes, techniques, equipment reviews, and culinary science.")
        self.add_website("https://www.goodreads.com", "Goodreads is a social cataloging website for book lovers to track reading, discover new titles, and connect with other readers.")
        self.add_website("https://www.audible.com", "Audible is an audiobook and podcast service owned by Amazon, offering thousands of titles across various genres.")
        self.add_website("https://www.archive.org", "Internet Archive is a digital library offering free access to millions of books, movies, music, and archived web pages.")
        self.add_website("https://www.deviantart.com", "DeviantArt is an online art community where artists showcase their work, connect with others, and sell prints and digital art.")
        self.add_website("https://www.artstation.com", "ArtStation is a portfolio platform for games, film, media, and entertainment artists to showcase professional work and connect with studios.")
        self.add_website("https://www.behance.net", "Behance is a creative portfolio platform where designers, illustrators, and artists display projects and discover creative talent.")
        self.add_website("https://www.dribbble.com", "Dribbble is a community for designers to share screenshots of their work, process, and projects for feedback and inspiration.")
        self.add_website("https://www.unsplash.com", "Unsplash is a photography website offering freely usable high-resolution photos contributed by photographers worldwide.")
        self.add_website("https://www.pexels.com", "Pexels is a free stock photo and video platform providing high-quality visual content for personal and commercial use.")
        self.add_website("https://www.shutterstock.com", "Shutterstock is a stock photography, footage, and music marketplace offering millions of licensed images for creative projects.")
        self.add_website("https://www.gettyimages.com", "Getty Images is a visual media company supplying stock images, editorial photography, video, and music licensing to businesses.")
        self.add_website("https://www.500px.com", "500px is a photography community where photographers share their work, discover inspiring images, and license their photos.")
        self.add_website("https://www.flickr.com", "Flickr is an image and video hosting platform where photographers organize, share, and discover visual content from around the world.")
        self.add_website("https://www.imgur.com", "Imgur is an online image sharing and hosting service where users upload, share, and browse funny and interesting images.")
        self.add_website("https://www.giphy.com", "Giphy is a searchable database and platform for sharing animated GIFs, stickers, and short video clips across social media.")
        self.add_website("https://www.vimeo.com", "Vimeo is a video hosting platform known for high-quality content, creative community, and professional video tools.")
        self.add_website("https://www.dailymotion.com", "Dailymotion is a video sharing platform offering user-generated and professional content across entertainment, news, and sports.")
        self.add_website("https://www.ted.com", "TED is a nonprofit devoted to spreading ideas through short, powerful talks on science, business, global issues, and creativity.")
        self.add_website("https://www.codecademy.com", "Codecademy is an online platform offering interactive coding courses in various programming languages and web development technologies.")
        self.add_website("https://www.freecodecamp.org", "freeCodeCamp is a nonprofit community offering free coding lessons, projects, and certifications in web development.")
        self.add_website("https://www.hackerrank.com", "HackerRank is a technical assessment and coding challenge platform used by developers to practice skills and by companies to hire talent.")
        self.add_website("https://www.leetcode.com", "LeetCode is a platform for preparing technical coding interviews with thousands of algorithm and data structure problems.")
        self.add_website("https://www.codewars.com", "Codewars is a coding challenge platform where developers train on kata, created by the community, to improve programming skills.")
        self.add_website("https://www.kaggle.com", "Kaggle is a data science competition platform offering datasets, notebooks, and community resources for machine learning practitioners.")
        self.add_website("https://www.topcoder.com", "Topcoder is a crowdsourcing company connecting businesses with a global community of designers, developers, and data scientists.")
        self.add_website("https://www.gitlab.com", "GitLab is a web-based DevOps platform providing source code management, CI/CD pipelines, and project collaboration tools.")
        self.add_website("https://www.bitbucket.org", "Bitbucket is a Git-based source code repository hosting service offering version control and collaboration tools for development teams.")
        self.add_website("https://www.docker.com", "Docker is a platform for developing, shipping, and running applications in containers, enabling consistent environments across systems.")
        self.add_website("https://www.kubernetes.io", "Kubernetes is an open-source container orchestration platform automating deployment, scaling, and management of containerized applications.")
        self.add_website("https://www.jenkins.io", "Jenkins is an open-source automation server used for continuous integration and continuous delivery of software projects.")
        self.add_website("https://www.atlassian.com", "Atlassian is a software company providing collaboration tools like Jira, Confluence, and Bitbucket for teams and enterprises.")
        self.add_website("https://www.asana.com", "Asana is a work management platform helping teams organize, track, and manage projects and tasks with visual workflows.")
        self.add_website("https://www.monday.com", "Monday.com is a work operating system enabling teams to run projects and workflows with customizable boards and automation.")
        self.add_website("https://www.basecamp.com", "Basecamp is a project management and team communication tool designed to keep work organized and conversations on track.")
        self.add_website("https://www.airtable.com", "Airtable is a cloud collaboration service combining the simplicity of spreadsheets with the power of databases for project tracking.")
        self.add_website("https://www.evernote.com", "Evernote is a note-taking and organization app allowing users to capture, organize, and find information across devices.")
        self.add_website("https://www.onenote.com", "OneNote is Microsoft's digital notebook allowing users to gather notes, drawings, screen clippings, and audio commentaries.")
        self.add_website("https://www.googledrive.com", "Google Drive is a cloud storage service enabling users to store files, sync across devices, and collaborate on documents.")
        self.add_website("https://www.onedrive.com", "OneDrive is Microsoft's cloud storage service integrated with Office 365, allowing file storage, sharing, and collaboration.")
        self.add_website("https://www.box.com", "Box is a cloud content management platform offering secure file storage, sharing, and collaboration for businesses.")
        self.add_website("https://www.mega.nz", "MEGA is a cloud storage and file hosting service emphasizing security with end-to-end encryption for stored data.")
        self.add_website("https://www.wetransfer.com", "WeTransfer is a file transfer service allowing users to send large files quickly and easily without registration.")
        self.add_website("https://www.grammarly.com", "Grammarly is a writing assistant using AI to check grammar, spelling, punctuation, and style across various platforms.")
        self.add_website("https://www.deepl.com", "DeepL is an advanced neural machine translation service offering high-quality translations in multiple languages.")
        self.add_website("https://www.translate.google.com", "Google Translate is a free multilingual translation service instantly translating text, speech, images, and web pages.")
        self.add_website("https://www.duolingo.com", "Duolingo is a free language learning platform offering courses in over 30 languages through bite-sized lessons and games.")
        self.add_website("https://www.memrise.com", "Memrise is a language learning platform using spaced repetition and mnemonic techniques to help users learn vocabulary.")
        self.add_website("https://www.busuu.com", "Busuu is a language learning community offering courses in 12 languages with interactive lessons and feedback from native speakers.")
        self.add_website("https://www.babbel.com", "Babbel is a subscription-based language learning app offering courses designed by linguists in 14 languages.")
        self.add_website("https://www.rosettastone.com", "Rosetta Stone is a language learning software using immersive methods to teach reading, writing, speaking, and listening skills.")
        self.add_website("https://www.meetup.com", "Meetup is a social networking platform for organizing and joining local groups based on shared interests and activities.")
        self.add_website("https://www.eventbrite.com", "Eventbrite is an event management and ticketing platform allowing organizers to create, promote, and sell tickets to events.")
        self.add_website("https://www.craigslist.org", "Craigslist is a classified advertisements website featuring sections for jobs, housing, items for sale, services, and community posts.")
        self.add_website("https://www.zillow.com", "Zillow is an online real estate marketplace providing home value estimates, listings, and tools for buyers, sellers, and renters.")
        self.add_website("https://www.realtor.com", "Realtor.com is a real estate listing website operated by the National Association of Realtors featuring homes for sale and rent.")
        self.add_website("https://www.redfin.com", "Redfin is a technology-powered real estate brokerage offering online tools and agent services for buying and selling homes.")
        self.add_website("https://www.trulia.com", "Trulia is a real estate website providing information on homes for sale and rent, neighborhood insights, and market trends.")
        self.add_website("https://www.apartments.com", "Apartments.com is a rental listing service featuring apartment and home rentals with photos, pricing, and neighborhood information.")
        self.add_website("https://www.indeed.com", "Indeed is a job search engine aggregating listings from thousands of websites, company career pages, and job boards worldwide.")
        self.add_website("https://www.glassdoor.com", "Glassdoor is a job and recruiting site featuring company reviews, salary reports, interview questions, and job listings.")
        self.add_website("https://www.monster.com", "Monster is an online employment solution for people seeking jobs and employers who need qualified candidates.")
        self.add_website("https://www.ziprecruiter.com", "ZipRecruiter is a job distribution and applicant tracking service connecting job seekers with employers through smart matching technology.")
        self.add_website("https://www.careerbuilder.com", "CareerBuilder is an employment website providing job listings, resume posting, and career advice for job seekers.")
        self.add_website("https://www.upwork.com", "Upwork is a freelancing platform connecting businesses with independent professionals for project-based and ongoing work.")
        self.add_website("https://www.fiverr.com", "Fiverr is an online marketplace for freelance services where sellers offer tasks and services starting at five dollars.")
        self.add_website("https://www.freelancer.com", "Freelancer is a crowdsourcing marketplace connecting employers with freelancers for projects in programming, design, writing, and more.")
        self.add_website("https://www.toptal.com", "Toptal is an exclusive network connecting companies with the top 3% of freelance software developers, designers, and finance experts.")
        self.add_website("https://www.99designs.com", "99designs is a graphic design platform connecting businesses with designers through contests and one-to-one projects.")
        self.add_website("https://www.wework.com", "WeWork is a coworking space provider offering flexible workspace solutions for entrepreneurs, freelancers, and established companies.")
        self.add_website("https://www.regus.com", "Regus provides flexible workspace solutions including coworking, private offices, and meeting rooms in locations worldwide.")
        self.add_website("https://www.hubspot.com", "HubSpot is an inbound marketing, sales, and customer service platform helping businesses attract visitors, convert leads, and close customers.")
        self.add_website("https://www.salesforce.com", "Salesforce is a cloud-based customer relationship management platform helping businesses connect with customers and manage sales processes.")
        self.add_website("https://www.mailchimp.com", "Mailchimp is an all-in-one marketing platform offering email marketing, automation, and audience management tools for businesses.")
        self.add_website("https://www.constantcontact.com", "Constant Contact is an email marketing platform providing tools for creating campaigns, managing contacts, and tracking results.")
        self.add_website("https://www.sendinblue.com", "Sendinblue is a digital marketing platform offering email marketing, SMS campaigns, and marketing automation for businesses.")
        self.add_website("https://www.hootsuite.com", "Hootsuite is a social media management platform allowing users to schedule posts, track analytics, and manage multiple social accounts.")
        self.add_website("https://www.buffer.com", "Buffer is a social media management tool enabling users to schedule posts, analyze performance, and manage multiple social media accounts.")
        self.add_website("https://www.sproutsocial.com", "Sprout Social is a social media management and optimization platform for businesses to manage presence and analyze performance.")
        self.add_website("https://www.later.com", "Later is a social media scheduling platform specializing in Instagram, allowing visual planning, scheduling, and analytics.")
        self.add_website("https://www.semrush.com", "SEMrush is an online visibility management platform providing tools for SEO, content marketing, competitor research, and PPC advertising.")
        self.add_website("https://www.ahrefs.com", "Ahrefs is an SEO toolset for backlink analysis, keyword research, competitor analysis, and site auditing for digital marketers.")
        self.add_website("https://www.moz.com", "Moz is an SEO software company providing tools and resources for search engine optimization, link building, and keyword research.")
        self.add_website("https://www.googleanalytics.com", "Google Analytics is a web analytics service tracking and reporting website traffic, user behavior, and conversion metrics.")
        self.add_website("https://www.hotjar.com", "Hotjar is a behavior analytics tool providing heatmaps, session recordings, and feedback polls to understand user behavior.")
        self.add_website("https://www.optimizely.com", "Optimizely is a digital experience platform offering A/B testing, personalization, and experimentation tools for websites and apps.")
        self.add_website("https://www.unbounce.com", "Unbounce is a landing page builder enabling marketers to create, publish, and optimize landing pages without developer help.")
        self.add_website("https://www.clickfunnels.com", "ClickFunnels is a sales funnel builder helping businesses market, sell, and deliver products online with automated funnels.")
        self.add_website("https://www.stripe.com", "Stripe is a payment processing platform for online businesses offering APIs and tools to accept and manage payments.")
        self.add_website("https://www.square.com", "Square provides payment processing hardware and software, helping businesses accept card payments and manage operations.")
        self.add_website("https://www.quickbooks.com", "QuickBooks is accounting software for small businesses offering features for invoicing, expense tracking, and financial reporting.")
        self.add_website("https://www.xero.com", "Xero is cloud-based accounting software for small businesses providing tools for invoicing, bank reconciliation, and bookkeeping.")
        self.add_website("https://www.freshbooks.com", "FreshBooks is cloud accounting software designed for small business owners and freelancers to manage invoicing and expenses.")
        self.add_website("https://www.wave.com", "Wave is free financial software for small businesses offering invoicing, accounting, and receipt scanning tools.")
        self.add_website("https://www.mint.com", "Mint is a personal finance management app helping users track spending, create budgets, and monitor credit scores.")
        self.add_website("https://www.personalcapital.com", "Personal Capital is a financial planning and wealth management service offering investment tracking and retirement planning tools.")
        self.add_website("https://www.ynab.com", "YNAB (You Need A Budget) is a budgeting app teaching users to gain control of money through proactive budget management.")
        self.add_website("https://www.robinhood.com", "Robinhood is a commission-free stock trading and investing app providing access to stocks, ETFs, options, and cryptocurrencies.")
        self.add_website("https://www.coinbase.com", "Coinbase is a cryptocurrency exchange platform allowing users to buy, sell, and store digital currencies securely.")
        self.add_website("https://www.binance.com", "Binance is a global cryptocurrency exchange offering trading in hundreds of digital currencies with advanced features.")
        self.add_website("https://www.kraken.com", "Kraken is a cryptocurrency exchange providing spot and futures trading, staking, and margin trading for digital assets.")
        self.add_website("https://www.blockchain.com", "Blockchain.com is a cryptocurrency wallet and exchange platform offering secure storage and trading of digital assets.")
        self.add_website("https://www.metamask.io", "MetaMask is a cryptocurrency wallet browser extension allowing users to interact with Ethereum blockchain applications.")
        self.add_website("https://www.opensea.io", "OpenSea is the largest NFT marketplace where users can discover, collect, and sell non-fungible tokens and digital art.")
        self.add_website("https://www.rarible.com", "Rarible is a community-owned NFT marketplace enabling creators to mint, buy, and sell digital collectibles.")
        self.add_website("https://www.niftygateway.com", "Nifty Gateway is a premium NFT marketplace featuring drops from top artists and brands in digital art and collectibles.")
        self.add_website("https://www.foundation.app", "Foundation is an NFT platform connecting digital creators with collectors through curated artwork and limited editions.")
        self.add_website("https://www.superrare.com", "SuperRare is a digital art marketplace for collecting and trading unique, single-edition digital artworks as NFTs.")
        self.add_website("https://www.unity.com", "Unity is a cross-platform game engine and development platform used for creating 2D, 3D, VR, and AR experiences.")
        self.add_website("https://www.unrealengine.com", "Unreal Engine is a powerful game engine and real-time 3D creation tool used for games, simulations, and visualization.")
        self.add_website("https://www.godotengine.org", "Godot is an open-source game engine providing tools for creating 2D and 3D games across multiple platforms.")
        self.add_website("https://www.itch.io", "Itch.io is an indie game marketplace where developers can upload, sell, and distribute games directly to players.")
        self.add_website("https://www.humblebundle.com", "Humble Bundle is a digital storefront offering game bundles, books, and software with portions supporting charity.")
        self.add_website("https://www.gog.com", "GOG (Good Old Games) is a digital distribution platform offering DRM-free video games and movies with a focus on classics.")
        self.add_website("https://www.epicgames.com", "Epic Games is a gaming company operating a digital storefront and offering free games, while developing Fortnite and Unreal Engine.")
        self.add_website("https://www.origin.com", "Origin is EA's digital distribution platform for purchasing and playing Electronic Arts games on PC and Mac.")
        self.add_website("https://www.uplay.com", "Uplay is Ubisoft's digital distribution platform providing access to Ubisoft games, rewards, and social features.")
        self.add_website("https://www.battlenet.com", "Battle.net is Blizzard Entertainment's online gaming service and digital distribution platform for their game titles.")
        self.add_website("https://www.playstation.com", "PlayStation is Sony's gaming brand featuring consoles, exclusive games, and online services for gaming enthusiasts.")
        self.add_website("https://www.xbox.com", "Xbox is Microsoft's gaming platform offering consoles, Game Pass subscription, and cross-platform gaming experiences.")
        self.add_website("https://www.nintendo.com", "Nintendo is a gaming company offering consoles like the Switch and creating iconic game franchises and characters.")
        self.add_website("https://www.minecraft.net", "Minecraft is a sandbox video game allowing players to build, explore, and survive in procedurally generated blocky worlds.")
        self.add_website("https://www.roblox.com", "Roblox is an online platform where users can create, share, and play games created by other users in a virtual universe.")
        self.add_website("https://www.fortnite.com", "Fortnite is a free-to-play battle royale game featuring building mechanics, creative modes, and collaborative gameplay.")
        self.add_website("https://www.leagueoflegends.com", "League of Legends is a multiplayer online battle arena game where teams compete in strategic matches with unique champions.")
        self.add_website("https://www.dota2.com", "Dota 2 is a free-to-play multiplayer online battle arena game with complex strategy and competitive esports scene.")
        self.add_website("https://www.callofduty.com", "Call of Duty is a first-person shooter franchise offering fast-paced multiplayer, battle royale, and campaign experiences.")
        self.add_website("https://www.overwatch.com", "Overwatch is a team-based multiplayer first-person shooter featuring diverse heroes with unique abilities and roles.")
        self.add_website("https://www.valorant.com", "Valorant is a free-to-play tactical first-person shooter combining precise gunplay with unique character abilities.")