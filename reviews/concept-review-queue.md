# Concept-tag adjudication queue (dual-pass)

Units compared: 208 — agreement 118 (56.7%). Each row below is a disagreement between two independent model passes; a human ruling resolves it (record rulings in reviews/concept-decisions-<date>.yaml).

| # | Instrument | Unit | Pass A | Pass B |
|---|---|---|---|---|
| 1 | nat/fra/loi-operations-spatiales-2008 | Art. 1 | (untagged by A) | ['liability_and_damage'] |
| 2 | nat/fra/loi-operations-spatiales-2008 | Art. 11-1 | ['state_responsibility_and_supervision'] | [] |
| 3 | nat/fra/loi-operations-spatiales-2008 | Art. 14 | ['international_cooperation_and_transparency', 'liability_and_damage'] | ['liability_and_damage'] |
| 4 | nat/fra/loi-operations-spatiales-2008 | Art. 2 | ['jurisdiction_and_control', 'state_responsibility_and_supervision'] | ['state_responsibility_and_supervision'] |
| 5 | nat/fra/loi-operations-spatiales-2008 | Art. 20-1 | ['state_responsibility_and_supervision'] | [] |
| 6 | nat/fra/loi-operations-spatiales-2008 | Art. 25-1 | ['state_responsibility_and_supervision'] | [] |
| 7 | nat/fra/loi-operations-spatiales-2008 | Art. 27 | ['state_responsibility_and_supervision'] | [] |
| 8 | nat/fra/loi-operations-spatiales-2008 | Art. 6 | ['liability_and_damage'] | ['liability_and_damage', 'state_responsibility_and_supervision'] |
| 9 | nat/fra/loi-operations-spatiales-2008 | Art. 7 | ['safety_of_space_operations', 'state_responsibility_and_supervision'] | ['state_responsibility_and_supervision'] |
| 10 | nat/fra/loi-operations-spatiales-2008 | Art. 9 | ['environmental_protection_and_debris', 'state_responsibility_and_supervision'] | ['state_responsibility_and_supervision'] |
| 11 | nat/lux/ressources-espace-2017 | Art. 1er | ['non_appropriation', 'resource_rights'] | ['resource_rights'] |
| 12 | nat/lux/ressources-espace-2017 | Art. 10 | (untagged by A) | ['liability_and_damage', 'state_responsibility_and_supervision'] |
| 13 | nat/lux/ressources-espace-2017 | Art. 11 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 14 | nat/lux/ressources-espace-2017 | Art. 12 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 15 | nat/lux/ressources-espace-2017 | Art. 14 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 16 | nat/lux/ressources-espace-2017 | Art. 2 | ['international_cooperation_and_transparency', 'state_responsibility_and_supervision'] | ['state_responsibility_and_supervision'] |
| 17 | nat/lux/ressources-espace-2017 | Art. 4 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 18 | nat/lux/ressources-espace-2017 | Art. 5 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 19 | nat/lux/ressources-espace-2017 | Art. 6 | (untagged by A) | ['state_responsibility_and_supervision'] |
| 20 | nat/usa/space-resources-2015 | §51302 Commercial exploration and commercial recovery | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency', 'resource_rights', 'state_responsibility_and_supervision'] | ['freedom_of_exploration_and_use', 'resource_rights', 'state_responsibility_and_supervision'] |
| 21 | un/ga/res-1962-XVIII | Paragraph 1 | ['freedom_of_exploration_and_use', 'non_appropriation'] | ['freedom_of_exploration_and_use'] |
| 22 | un/ga/res-1962-XVIII | Paragraph 6 | ['environmental_protection_and_debris', 'international_cooperation_and_transparency'] | ['dispute_settlement_and_consultation', 'environmental_protection_and_debris', 'international_cooperation_and_transparency'] |
| 23 | un/ga/res-37-92 | (granularity) | ['dispute_settlement_and_consultation', 'international_cooperation_and_transparency', 'peaceful_use_and_non_militarization', 'state_responsibility_and_supervision'] | per-unit tags (see pass-B.json) |
| 24 | un/ga/res-41-65 | Principle II | (untagged by A) | ['freedom_of_exploration_and_use'] |
| 25 | un/ga/res-41-65 | Principle IV | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency'] | ['freedom_of_exploration_and_use'] |
| 26 | un/ga/res-41-65 | Principle IX | (untagged by A) | ['international_cooperation_and_transparency', 'registration'] |
| 27 | un/ga/res-41-65 | Principle V | (untagged by A) | ['international_cooperation_and_transparency'] |
| 28 | un/ga/res-41-65 | Principle VI | (untagged by A) | ['international_cooperation_and_transparency'] |
| 29 | un/ga/res-41-65 | Principle VII | (untagged by A) | ['international_cooperation_and_transparency'] |
| 30 | un/ga/res-41-65 | Principle VIII | (untagged by A) | ['international_cooperation_and_transparency'] |
| 31 | un/ga/res-41-65 | Principle X | ['environmental_protection_and_debris'] | ['environmental_protection_and_debris', 'international_cooperation_and_transparency'] |
| 32 | un/ga/res-41-65 | Principle XI | ['environmental_protection_and_debris', 'international_cooperation_and_transparency'] | ['international_cooperation_and_transparency'] |
| 33 | un/ga/res-41-65 | Principle XII | ['international_cooperation_and_transparency', 'resource_rights'] | ['international_cooperation_and_transparency'] |
| 34 | un/ga/res-41-65 | Principle XIII | ['international_cooperation_and_transparency'] | ['dispute_settlement_and_consultation', 'international_cooperation_and_transparency'] |
| 35 | un/ga/res-47-68 | Principle 10 | (untagged by A) | ['dispute_settlement_and_consultation'] |
| 36 | un/ga/res-47-68 | Principle 2 | ['environmental_protection_and_debris', 'safety_of_space_operations'] | [] |
| 37 | un/ga/res-47-68 | Principle 4 | ['safety_of_space_operations'] | ['international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 38 | un/ga/res-47-68 | Principle 6 | ['international_cooperation_and_transparency'] | ['dispute_settlement_and_consultation', 'international_cooperation_and_transparency'] |
| 39 | un/ga/res-47-68 | Principle 7 | ['international_cooperation_and_transparency'] | ['international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 40 | un/ga/res-51-122 | (granularity) | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency', 'non_appropriation'] | per-unit tags (see pass-B.json) |
| 41 | un/softlaw/copuos-debris-mitigation-2007 | Guideline 4 | ['environmental_protection_and_debris', 'peaceful_use_and_non_militarization'] | ['environmental_protection_and_debris', 'safety_of_space_operations'] |
| 42 | un/softlaw/copuos-debris-mitigation-2007 | Guideline 5 | ['environmental_protection_and_debris'] | ['environmental_protection_and_debris', 'safety_of_space_operations'] |
| 43 | un/softlaw/lts-guidelines-2019 | Guideline A.4 | ['international_cooperation_and_transparency', 'safety_of_space_operations'] | ['international_cooperation_and_transparency'] |
| 44 | un/softlaw/lts-guidelines-2019 | Guideline B.6 | ['safety_of_space_operations'] | ['international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 45 | un/softlaw/lts-guidelines-2019 | Guideline B.7 | ['safety_of_space_operations'] | ['international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 46 | un/softlaw/lts-guidelines-2019 | Guideline B.8 | ['environmental_protection_and_debris', 'safety_of_space_operations'] | ['safety_of_space_operations'] |
| 47 | un/softlaw/lts-guidelines-2019 | Guideline B.9 | ['environmental_protection_and_debris', 'safety_of_space_operations'] | ['international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 48 | un/softlaw/lts-guidelines-2019 | Guideline D.1 | ['international_cooperation_and_transparency', 'safety_of_space_operations'] | ['environmental_protection_and_debris', 'international_cooperation_and_transparency'] |
| 49 | un/treaty/liability-1972 | Article IX | ['dispute_settlement_and_consultation', 'liability_and_damage'] | ['liability_and_damage'] |
| 50 | un/treaty/liability-1972 | Article VIII | ['dispute_settlement_and_consultation', 'liability_and_damage'] | ['liability_and_damage'] |
| 51 | un/treaty/liability-1972 | Article X | ['dispute_settlement_and_consultation', 'liability_and_damage'] | ['liability_and_damage'] |
| 52 | un/treaty/liability-1972 | Article XII | ['dispute_settlement_and_consultation', 'liability_and_damage'] | ['liability_and_damage'] |
| 53 | un/treaty/liability-1972 | Article XIII | (untagged by A) | ['liability_and_damage'] |
| 54 | un/treaty/liability-1972 | Article XIV | ['dispute_settlement_and_consultation'] | ['dispute_settlement_and_consultation', 'liability_and_damage'] |
| 55 | un/treaty/liability-1972 | Article XVI | (untagged by A) | ['dispute_settlement_and_consultation'] |
| 56 | un/treaty/liability-1972 | Article XVII | (untagged by A) | ['dispute_settlement_and_consultation'] |
| 57 | un/treaty/liability-1972 | Article XX | (untagged by A) | ['dispute_settlement_and_consultation'] |
| 58 | un/treaty/liability-1972 | Article XXI | ['international_cooperation_and_transparency', 'liability_and_damage'] | ['international_cooperation_and_transparency'] |
| 59 | un/treaty/moon-1979 | Article 10 | ['rescue_and_return'] | ['rescue_and_return', 'safety_of_space_operations'] |
| 60 | un/treaty/moon-1979 | Article 12 | ['jurisdiction_and_control'] | ['abandonment_and_salvage', 'jurisdiction_and_control'] |
| 61 | un/treaty/moon-1979 | Article 13 | ['international_cooperation_and_transparency'] | ['abandonment_and_salvage', 'international_cooperation_and_transparency'] |
| 62 | un/treaty/moon-1979 | Article 14 | ['state_responsibility_and_supervision'] | ['liability_and_damage', 'state_responsibility_and_supervision'] |
| 63 | un/treaty/moon-1979 | Article 2 | ['peaceful_use_and_non_militarization'] | ['international_cooperation_and_transparency', 'peaceful_use_and_non_militarization'] |
| 64 | un/treaty/moon-1979 | Article 9 | ['international_cooperation_and_transparency', 'jurisdiction_and_control'] | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency'] |
| 65 | un/treaty/ost-1967 | Article I | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency', 'non_appropriation'] | ['freedom_of_exploration_and_use', 'international_cooperation_and_transparency'] |
| 66 | un/treaty/registration-1975 | Article VI | ['abandonment_and_salvage', 'international_cooperation_and_transparency', 'registration'] | ['international_cooperation_and_transparency', 'liability_and_damage', 'registration'] |
| 67 | un/treaty/rescue-1968 | Article 2 | ['rescue_and_return'] | ['international_cooperation_and_transparency', 'rescue_and_return'] |
| 68 | un/treaty/rescue-1968 | Article 5 | ['abandonment_and_salvage', 'international_cooperation_and_transparency', 'liability_and_damage'] | ['abandonment_and_salvage', 'international_cooperation_and_transparency', 'safety_of_space_operations'] |
| 69 | un/treaty/rescue-1968 | Article 6 | ['state_responsibility_and_supervision'] | [] |
