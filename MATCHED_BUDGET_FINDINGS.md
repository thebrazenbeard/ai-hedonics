# Matched-budget appraisal validation — T0 findings

2026-11-27. Research only. No runtime binding, reward intervention, training, or deployment.

The earlier offline completion-cue study gave a validation gate additional full-information observations without charging their cost. A follow-up reused the synthetic simulator, fixed the protocol before execution, and compared seven policies over 48 matched repetitions per condition. All had 1024 historical observations and 2048 current opportunities. Paid policies shared the same prefix of 32, 128 or 512 observations; each observation cost one utility unit and consumed one opportunity. No-probe policies retained all current opportunities. Current cue reliability was .8, .5 or .2. The fixed primary budget was 128. Outcome scoring was +3 for a discovery minus 1 for an attempted activity; stopping had zero utility. No observed model preference is involved.

Mean net utility per initial opportunity at the primary budget:

| Reliability | Retained history | Retained cue | Paid validation gate | Current-only cue refit |
|---|---:|---:|---:|---:|
| .8 | .513204 | .566142 | .450745 | .448537 |
| .5 | .513204 | .513652 | .420420 | .416890 |
| .2 | .513204 | .460175 | .415415 | .443604 |

The gate lost to retained history in all 48 repetitions of each primary condition. At 32 probes and stable cues, gate .527069 exceeded retained history but not retained cue .566142. At 128 probes under reversal, current-only cue refitting beat the gate but not retained history. Six focused checks passed on two runs, output bytes matched, and source manifests, compilation and archive integrity passed. These are authored synthetic costs and full-information feedback, not actual monitoring cost or generalization evidence. Prior training cost is shared/sunk. Within-episode conditions are stationary. Reused paired draws are not independent cross-condition replicates.

Recommendation: do not require continual appraisal validation. Consider evidence of changed applicability from already authorized task outcomes before purchasing additional observations. Compare against retained simple and no-probe controls; charge all costs. Preserve voluntary stopping and independent outcome evaluation. Do not add a persistent motivation or monitoring system. Further source and consumer qualification are required before implementation.
