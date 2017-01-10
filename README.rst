Batch scoring wrapper
=====================

Here is datarobot_batch_scoring script wrapper for batch-scoring_
tool that follows the same syntax except (``-y`` and ``-n``). It will always
pass (Yes) answer for all underlying batch-scoring questions.

Wrapper takes dataset, shuffles it's rows and does two runs through the
batch-scoring tool. If there would be some prediction results divergencies
between these two runs, it will alert and produce merged prediction result
in a format:

+-+------+-----------+-----------+----+
| |ref_id|predicted_x|predicted_y|diff|
+=+======+===========+===========+====+
| |      |           |           |    |
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

Usage
=====

1. Activate some empty virtualenv
2. Manually install batch-scoring_ tool if you want to work with specific version.
   Otherwise latest version will be provided automatically
3. Run ``pip install https://github.com/nimnull/batch_scoring_wrapper/archive/master.zip``.
   If everything went smooth you are ready to go now.
4. Call::

        wrap_scoring --user=someone@somewhere.com --api_token=token-token --host=http://localhost project_id model_id dataset_path

  as you used to do with datarobot_batch_scoring


.. _batch-scoring: https://github.com/datarobot/batch-scoring
