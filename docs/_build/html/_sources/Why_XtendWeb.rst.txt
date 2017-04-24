Why you should use XtendWeb
===============================

You might have seen web host's marketing themselves to be stable because they use CloudLinux or similar technologies

Here  is why the Idea is fundamentally flawed:
-------------------------------------------------
1. CloudLinux basically act as a choke or speed breaker to your website
2. This is good from a webHosts point of view but not from the point of view of an enterprise
3. enterprise needs the ability to use more resources when a need arise rather than having someone put a speed breaker
4. Enterprise need scalable hosting infrastructure which can scale out (not up)

Ok, I need scalable hosting, so what are my options?
-----------------------------------------------------

1. Spend money on cloud and human resource and build a cloud-native application
2. Deploy the app in a private or public cloud using technologies like Kubernetes that can scale your cloud-native app
3. or find a hosted PaaS equivalent for your app and start using it (your provider will look into the scaling side)

What if all I need to do is host a web app like WordPress?
------------------------------------------------------------

1. Creating an OpenStack cloud and deploying your WordPress web app in Kubernetes will be an overkill
2. As an SME you should opt for a simpler deployment model than can scale to a certain extend too and that your existing human resources can use without additional training

Can you describe more?
-------------------------
common web application are mostly three tiered ( https://en.wikipedia.org/wiki/Multitier_architecture#Web_development_usage )
and can be easily scaled by pooling more web,application and database servers .
XtendWeb offers you the ability to host your web applications across multiple servers , that are DNS loadbalanced
This offers room to grow as your site will be deployed in multiple servers that work in tandem
This is xtreme opposite to having a choke or speed-breaker be put to limit your resource .

As a webHost , how does this help my business?
-------------------------------------------------
As a webhost you can design premium plans that offer clustered hosting service that will be perfect for enterprise customers
who need more resources and prefer high availability


As an enterprise user how does this help me?
-------------------------------------------------
You get simple hosting solution that use the familiar cPanel control panel and transparently does clustering and multi web server
application deploymet . You dont need new training or human resource to manage the hosting as the end user hosting experiance of using
a cPanel account remain the same even with a high performing , multi webserver cluster with no speed-brakes are working in the backgound
to host your e-commerce store frontend or company website.

You can already find a list of webHosts that offer such premium service at https://xtendweb.gnusys.net/Nginx_friendly_web_hosts.html
