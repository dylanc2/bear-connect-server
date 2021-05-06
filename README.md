# Bear Connect

Members: Justin Norman, Dylan Chow, Elaine Wang, Hongyang Zheng, Nidhi Kakulawaram

We plan on building the backend for an app that connects students who are taking similar classes, so that they can form study groups. Users can create profiles that specify the classes they are taking, study habits, preferred meeting times, year, major, and hobbies. Users can choose to join an existing group, or start a group with another student. Students will be able to message each other directly on the platform. We plan on using FireBase for authentication and storing user data, and the Twilio chat API.

Run './demo.sh' in the project's root directory to start docker containers.

## TA's feedback 
* API: Twilio seems to charge you based on the APP's traffic, which needs your attention, but for just a school project, it should be okay. The API is well documented, but the branches of its services are a lot. Just pick the entry level one check the returned data structure/type before you use it.
* Scope: I suggest you focus on just one or two features. The interactivity part can be at a minimal level - you don't need all of them to demo your idea. On the other hand, how to incorporate Twilio and systematically organize data accessing/storage should be prioritized, in my opinion.
