Batch scoring wrapper
=====================

Here is datarobot_batch_scoring script wrapper for `batch-scoring
<https://github.com/datarobot/batch-scoring/>`_ tool that follows the same syntax
except (``-y`` and ``-n``). It suggest that (Yes) would be passed by default.

Wrapper takes dataset, shuffles it's rows and does two runs through the
batch-scoring tool. If there would be some prediction results divergencies
between these two runs, it will alert and produce merged prediction result
in a format:

+-+------+-----------+-----------+----+
| |ref_id|predicted_x|predicted_y|diff|
+-+------+-----------+-----------+----+

Where:

ref_id
    is an original dataset row number (passed to the wrapper script, unshuffled)

predicted_x
    prediction result from the first shuffled attempt

predicted_y
    prediction result from the second shuffled attempt

diff
    predicted_x - predicted_y

In case the were no differences between predictions ``out.csv`` produced.
Otherwise predictions & differences are saved into ``diverged.csv`` file.
