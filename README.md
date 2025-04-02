# ChickenHat Bot

This is silly hack, on a cheap show prize!

Hat Demo here -> https://www.youtube.com/shorts/uD40l2RZySg

Twitch Redeem Demo -> https://youtube.com/shorts/_8AXoxJZ9SM

A purely hacked together piece of code to automatically trigger the hat when the chickenhat reward is redeemed on [SsjSilentTV's](https://www.twitch.tv/ssjsilenttv) Twitch stream.

Uses Twitch EventSub WebSocket to listen for channel point redemptions and triggers the chicken hat.

## Environment Variables

- `TWITCH_CLIENT_ID`: Your Twitch application client ID
- `TWITCH_CLIENT_SECRET`: Your Twitch application client secret
- `TWITCH_USER_ID`: The broadcaster's Twitch user ID
- `OPENHAB_URL`: URL to your OpenHAB instance

## Build Details
- VL530X Time of Flight Sensor
- TinyPico MicroController by [Unexpected Maker](https://unexpectedmaker.com/)
- [Tasmota](https://github.com/arendst/Tasmota) for the IoT integration
