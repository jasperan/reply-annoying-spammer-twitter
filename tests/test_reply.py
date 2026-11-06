import unittest
from types import SimpleNamespace as NS
from unittest import mock

import reply

OWN = "1"
MSG = "hello"


def user(name, uid):
    return NS(screen_name=name, id_str=uid)


def mention(i, name="target"):
    return NS(id=i, user=user(name, "99" if name == "target" else "5"), created_at="t")


class FakeApi:
    def __init__(self, timeline, search=()):
        self.timeline = timeline
        self.search = list(search)
        self.posted = []
        self.timeline_calls = []

    def mentions_timeline(self, count, since_id=None):
        self.timeline_calls.append((count, since_id))
        items = [m for m in self.timeline if since_id is None or m.id > since_id]
        return sorted(items, key=lambda m: m.id, reverse=True)[:count]

    def search_tweets(self, **kw):
        return self.search

    def update_status(self, **kw):
        self.posted.append(kw)


class RespondTests(unittest.TestCase):
    def run_poll(self, api, state=None):
        with mock.patch.object(reply.time, "sleep"):
            reply.respond_to_mentions(api, "target", MSG, OWN, state)

    def test_third_party_copy_does_not_suppress_reply(self):
        fake = NS(in_reply_to_status_id=100, full_text=f"@target {MSG}", user=user("evil", "666"))
        api = FakeApi([mention(100)], [fake])
        self.run_poll(api)
        self.assertEqual(len(api.posted), 1)

    def test_own_reply_suppresses(self):
        own = NS(in_reply_to_status_id=100, full_text=f"@target {MSG}", user=user("me", OWN))
        api = FakeApi([mention(100)], [own])
        self.run_poll(api)
        self.assertEqual(api.posted, [])

    def test_burst_does_not_hide_target_mention(self):
        api = FakeApi([mention(100)] + [mention(i, "spam") for i in range(101, 106)])
        state = {}
        self.run_poll(api, state)
        self.assertEqual(len(api.posted), 1)

    def test_cursor_advances_and_failed_mention_is_retried(self):
        api = FakeApi([mention(100)])
        state = {}
        api.update_status = mock.Mock(side_effect=RuntimeError("boom"))
        with self.assertRaises(RuntimeError):
            self.run_poll(api, state)
        self.assertNotIn("since_id", state)
        api.update_status = lambda **kw: api.posted.append(kw)
        self.run_poll(api, state)
        self.assertEqual(len(api.posted), 1)
        self.assertEqual(state["since_id"], 100)
        self.run_poll(api, state)
        self.assertEqual(api.timeline_calls[-1], (reply.MENTIONS_PER_POLL, 100))


if __name__ == "__main__":
    unittest.main()
