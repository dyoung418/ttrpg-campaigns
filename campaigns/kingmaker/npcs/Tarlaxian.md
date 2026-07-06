---
type: npc
campaign: kingmaker
tags:
  - campaign/kingmaker
  - enemy
  - dragon
sources: []
related:
  - "[[Astor]]"
  - "[[Briar]]"
  - "[[House at the Edge of Time]]"
  - "[[Ilthuliak]]"
  - "[[Lee]]"
  - "[[Lucas]]"
  - "[[Nyrissa]]"
  - "[[Pavel]]"
  - "[[Riven]]"
  - "[[Session 100 - She Dropped Your Letter]]"
  - "[[Session 102 - The Undefeated]]"
  - "[[Session 103 - The Shape of Where I Used to Be]]"
  - "[[The Rimebridge]]"
  - "[[Thousandbreaths]]"
aliases: []
status: alive
role: "Tarn linnorm; guardian of the bridge to the House at the Edge of Time"
faction: "[[Nyrissa]] (loosely)"
location: "The Rimebridge — bridge to the House at the Edge of Time"
first_appeared: "Session 103 (planned)"
created: "2026-06-03"
---

# Tarlaxian

> **Role**: The wall on the bridge — a gargantuan tarn linnorm coiled at the far end of the span to the [[House at the Edge of Time]]
> **Creature 20** (uncommon) — run here with the boss modifications below, which push the effective threat well past a standard solo Creature 20
> **Status**: Alive; blocks the bridge but **won't pursue into the House**

## Summary

A gargantuan tarn linnorm who has claimed the bottomless dark lake beneath the [[House at the Edge of Time]] as its *tarn*. The far shore flickers between mountain ranges and open starfield. Tarlaxian guards the long stone bridge — the only crossing — and kills anything that tries to pass. It is **not loyal to [[Nyrissa]]** so much as territorial: she suffered it to den in her lake, and it pays the rent by drowning her unwanted guests. There is **no negotiation** — this is a pure wall (see Session 103 prep). It will not follow the party off the bridge into the House.

> [!note] Frost reskin
> The exported statblock is the standard **acid** tarn linnorm. For this campaign it is reskinned to **cold/frost** — damage type, breath, venom, and aura are all cold. Mechanics and DCs are unchanged; only the energy type and flavor differ. (Regeneration is still *deactivated by cold iron* — that's a material, not a damage type.)

---

## Statblock

**Creature 20** · Uncommon · CE · Gargantuan · **Cold**, Amphibious, Dragon

**Perception** +35; darkvision, scent (imprecise) 60 ft, **all-around vision**, *truesight* (constant)
**Languages** Aklo, Draconic, Fey

**Str** +10, **Dex** +6, **Con** +8, **Int** −1, **Wis** +7, **Cha** +8

**AC** 46 · **Fort** +36, **Ref** +32, **Will** +31 · **+1 status to all saves vs. magic**
**HP** 400; **Regeneration 15** (deactivated by cold iron); **Immunities** cold, curse, paralyzed, sleep

- **Reactive Strike (Tail Only)** — reaction; makes a Tail Strike against a triggering creature.
- ***Unfettered Movement* (constant)** — ignores circumstance penalties to Speed; auto-succeeds to Escape non-magical Immobilized/Grabbed/Restrained. **(The party can't easily grapple or pin *it*.)**

**Speed** 35 ft, fly 100 ft, swim 80 ft

**Melee** Jaws +38 (magical, reach 30) — **4d12+18 piercing** plus *Tarn Linnorm Frost-Venom*
**Melee** Claw +38 (agile, magical, reach 30) — **4d8+18 slashing**
**Melee** Tail +38 (agile, magical, reach 30) — **4d6+18 bludgeoning**

**Primal Innate Spells** DC 44, attack +34; **9th** *unfettered movement* (constant); **8th** *truesight* (constant)

- **Improved Grab** — free action after a Jaws hit.
- **Constrict** (1 action) — 3d6+18 bludgeoning, **DC 44 basic Fortitude**.
- **Double Bite** (1 action) — Stride, then a Jaws Strike with **each head** against two different targets; both count toward the MAP, but MAP doesn't increase until after both Strikes.
- **Rimebreath** *(Corrosive Breath, reskinned cold)* (2 actions) — a **120-ft line** or **60-ft cone** of killing frost, **20d6 cold**, **DC 44 basic Reflex**. Can't use Rimebreath or Double Breath again for **1d4 rounds**. The frost leaves a freezing mist: at the start of the linnorm's next turn, any creature that *failed* the Reflex save must succeed at **DC 42 Fortitude** or be **Sickened 4**.
- **Double Breath** (3 actions) — uses Rimebreath twice; a creature attempts only one save and takes damage only once. Can't use Rimebreath or Double Breath again for **2d4 rounds**.
- **Tarn Linnorm Frost-Venom** *(poison, reskinned cold)* — **DC 44 Fortitude**, max duration 10 rounds. **Stage 1** 7d6 cold + Drained 1 (1 round); **Stage 2** 11d6 cold + Drained 2 (1 round).
- **Curse of Death** — when a creature **slays** Tarlaxian, it must succeed at a **DC 46 Will** save or it can **no longer recover Hit Points by any means** (healing, Medicine, natural rest). Unlimited duration. *(The kill shot is a loaded decision — let someone realize this before they take it.)*

---

## Boss Modifications — Session 103 *(the action-economy fixes)*

> [!warning] GM Only — why these exist
> A lone Creature 20 against six honed PCs loses the action-economy war on numbers alone (the party found Ilthuliak + 9 stone guardians "tough but not scary-tough"). Tarlaxian is a **pure wall** — no adds — so its second front has to be **itself and the lake**. These layer on top of the statblock above.

### 1. Two turns per round *(core fix)*
Tarlaxian acts on its initiative **and again on initiative − 10**. This roughly doubles its action economy and is the load-bearing change. *Dial:* if it runs too hot, drop the second turn to a single extra action.

### 2. The bottomless lake is the real second combatant *(Amphibious; Swim 80)*
- **Submerge** (part of a Swim) — slips beneath the black water and becomes **Unseen**. This is the answer to **[[Riven]]**: no clean line of sight, no ranged alpha strike. The lake is its cover; it chooses when and where to surface. *(It still tracks the party via scent, truesight, and all-around vision — submerging blinds the party, not the linnorm.)*
- **Surge & Seize** — erupts from the lake adjacent to a chosen target on the span, Strike + **Improved Grab** on a hit. It dictates where the fight happens every round.
- **Coil Drag** *(the action-economy reverser)* — on a grabbed creature, it dives, dragging them **off the bridge into the bottomless freezing lake**. **Scary-but-recoverable:** the victim is drowning + taking cold, *removed from the fight*, and it costs **two other PCs' actions** to rescue them — but the bridge and [[Astor]] can always reach them; nobody is auto-lost. Target **Riven** or **[[Pavel]]**.

### 3. The Rimebridge *(extremely difficult terrain)*
The span is sheathed in black ice from the linnorm's breath and the freezing lake-spray.
- **Greater difficult terrain** — every 5 ft of movement costs an extra 10 ft. **Caps [[Lee]]** (a swashbuckler lives on movement/repositioning for Panache) and **forces the party to cluster** (feeds Tail Sweep and the breath).
- **Slide** — anyone **knocked prone or shoved** on the ice slides toward the nearest edge; **Reflex/Acrobatics** to catch the lip before the bottomless drop. Every knockback and Coil Drag becomes a *fall* threat, not just damage.

### 4. Frostbite Aura *(emanation)*
**Aura (cold), 5 feet.** A creature that enters the emanation, or that starts or ends its turn in it, takes **3d6 cold damage** (**DC 44 basic Fortitude**) and is **Slowed 1** until the end of its next turn. Punishes **Lee** and **Pavel** for crowding it — and if Pavel parks his mobile *silence* in melee to shut down casting, he's standing exactly where Coil Drag wants him.

> [!note] FoundryVTT implementation (PF2e 8.2.0)
> The damaging-aura-with-save-on-turn-end is **not natively automatable** — the system's Aura rule element only fires on `enter` (no turn-start/turn-end events yet; see foundryvtt/pf2e issue #7123). So this is split: **Slowed auto-applies via the aura; the cold damage + save is a click** off the description inline.
>
> **(a) Ability description** (paste into the Frostbite Aura ability's Description — gives the clickable damage + save):
> ```
> <strong>Aura</strong> (cold), 5 feet. A creature that enters the emanation, or that starts or ends its turn in the emanation, takes @Damage[3d6[cold]] (@Check[fortitude|dc:44|basic]) and is @UUID[Compendium.pf2e.conditionitems.Item.xYTAsEpcJE1Ccni3]{Slowed 1} until the end of its next turn.
> ```
>
> **(b) Aura rule element** (Rules tab — code view only; the visual editor silently drops the config). Draws the 5-ft cold ring and auto-applies the Frostbite effect to enemies:
> ```json
> [
>   {
>     "key": "Aura",
>     "slug": "frostbite-aura",
>     "radius": 5,
>     "traits": ["cold"],
>     "effects": [
>       { "uuid": "Item.Hhgbc9Ak4gY3duzH", "affects": "enemies", "removeOnExit": true }
>     ],
>     "appearance": {
>       "border": { "color": "#7fd4ff" },
>       "highlight": { "color": "#7fd4ff", "alpha": 0.25 }
>     }
>   }
> ]
> ```
>
> **(c) Effect: Frostbite** (the world Item the aura points at, `Item.Hhgbc9Ak4gY3duzH`) — one rule element granting Slowed 1:
> ```json
> [
>   {
>     "key": "GrantItem",
>     "uuid": "Compendium.pf2e.conditionitems.Item.xYTAsEpcJE1Ccni3",
>     "inMemoryOnly": true,
>     "alterations": [
>       { "mode": "override", "property": "badge-value", "value": "1" }
>     ]
>   }
> ]
> ```
>
> **At the table:** a creature in the ring is auto-Slowed 1 (clears on exit); when it enters or starts/ends its turn adjacent, click `@Damage` + `@Check` from the description. Caveat: because the system only fires on `enter`, the auto-Slowed rides "while adjacent" rather than literally "until end of next turn" — a clean approximation for a 5-ft melee aura.

### 5. Silence-proofing & the fascination valve *(counters the party's signature tools)*
- **[[Pavel]]'s mobile silence whiffs:** Rimebreath, Frost-Venom, Constrict, the Frostbite Aura, and Curse of Death are all **physical/non-verbal** — silence does nothing to them. *Unfettered movement* also means he can't pin it in place.
- **[[Lucas]]'s 9th-level fascination genuinely lands** (Will +31, +1 vs. magic = effectively +32 — its weakest save; not immune to mental). Don't flat-immunize it — the escape valve is thematic: **a fascinated linnorm simply submerges**, breaking line of sight and ending the effect. Fascination buys the party **one good round**, not the fight — same balance struck for Ilthuliak.

---

## Tactics

- **Opening:** Tarlaxian is already coiled at the far end when the party steps onto the Rimebridge (see the Session 103 cold open — [[Briar|Briara]] feels Nyrissa, then the head lifts from the dark water). Round 1, it leads with **Rimebreath** down the **120-ft line** — the bridge is narrow, so the clustered party eats it.
- **Sustain:** alternates **Double Bite** (two heads, two targets) and **Surge & Seize → Coil Drag** to peel a ranged PC into the lake; uses **Submerge** to deny Riven and reset position; **Reactive Strike (Tail)** punishes anyone who tries to stride past on the ice.
- **vs. melee:** the **Frostbite Aura** and **greater difficult terrain** make crowding it costly; *unfettered movement* stops the party from locking it down.
- **Resolve:** **fights as a wall** — no retreat off the bridge, no negotiation, no pursuit into the House. It dies on the span or the party doesn't cross. **Regeneration 15** means they need real damage (or **cold iron**) to keep it down. **Curse of Death** waits for whoever lands the kill.

---

## History & Motivation

Ancient even by linnorm standards, Tarlaxian came to the [[House at the Edge of Time]] long ago and claimed its bottomless lake as a *tarn* worthy of its kind. [[Nyrissa]] did not summon it and does not command it; she simply never troubled to evict a monster that drowns the champions who come for her. The arrangement suits them both. The bridge is the only crossing, and Tarlaxian regards everything on it as prey trespassing on its water.

---

## Related Notes

- [[House at the Edge of Time]]
- [[Thousandbreaths]]
- [[Nyrissa]]
- [[Ilthuliak]]
- [[Session 103]] *(prep)*
