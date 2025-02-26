from utils import *


def test_siamat():
    game = prepare_game()
    siamat = game.player1.give("ULD_178").play()
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    assert siamat.windfury
    assert siamat.divine_shield


def test_vulpera_scoundrel():
    game = prepare_empty_game()
    game.player1.give("ULD_209").play()
    choice = game.player1.choice
    assert len(choice.cards) == 4
    assert choice.cards[3].id == "ULD_209t"
    choice.choose(choice.cards[3])
    assert game.player1.hand[0].type == CardType.SPELL
    assert not game.player1.choice


def test_dwarven_archaeologist():
    game = prepare_empty_game()
    game.player1.give("ULD_309").play()
    game.player1.give("DAL_741").play()
    choice = game.player1.choice
    card = choice.cards[0]
    origin_cost = card.cost
    choice.choose(card)
    assert card.zone == Zone.HAND
    assert card.cost == max(origin_cost - 1, 0)


def test_evil_recruiter():
    game = prepare_game()
    recruiter = game.player1.give("ULD_162")
    assert not recruiter.requires_target()
    wisp = game.player1.summon(WISP)
    assert not recruiter.requires_target()
    lackey = game.player1.summon("DAL_613")
    assert recruiter.requires_target()
    assert wisp not in recruiter.targets
    assert lackey in recruiter.targets


def test_beeees():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    mech = game.player1.give(MECH).play()
    game.end_turn()
    game.player2.give("ULD_134").play(target=mech)
    assert game.player2.field == []
    assert mech.damage == 4
    game.player2.give("ULD_134").play(target=wisp)
    assert wisp.dead
    assert game.player2.field == ["ULD_134t"] * 3


def test_corrupt_the_waters():
    game = prepare_empty_game()
    game.player1.give("ULD_291").play()
    for _ in range(6):
        minion = game.player1.give("CS2_189").play(target=game.player2.hero)
        minion.destroy()
    assert game.player1.hero.power == "ULD_291p"
    game.skip_turn()
    assert not game.player1.extra_battlecries
    game.player1.hero.power.use()
    assert game.player1.extra_battlecries
    assert game.player2.hero.health == 24
    minion = game.player1.give("CS2_189").play(target=game.player2.hero)
    minion.destroy()
    assert game.player2.hero.health == 22
    minion = game.player1.give("CS2_189").play(target=game.player2.hero)
    assert game.player2.hero.health == 20
    minion.destroy()
    game.skip_turn()
    assert not game.player1.extra_battlecries


def test_sunstruck_henchman():
    game = prepare_empty_game()
    henchman = game.player1.give("ULD_180").play()
    game.skip_turn()
    while henchman.can_attack():
        game.skip_turn()
    assert not henchman.can_attack()


def test_bazaar_burglary():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    quest = game.player1.give("ULD_326").play()
    assert quest.progress == 0
    game.player1.give(MOONFIRE)
    assert quest.progress == 1
