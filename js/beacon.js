navigator.sendBeacon('http://localhost:3000', JSON.stringify({
    type: 'impressions',
    uid: 'uuid-or-smth-like-that',
    user_agent: 'Chrome V8',
    screen_x: '12',
    screen_y: '12',
}))
