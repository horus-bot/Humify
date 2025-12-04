from third_layer import human_imperfection_layer
from second_layer import rewrite_with_groq
from intent_extractor import extract_intent
from fourth_layer import humanize_with_groq


sample_original = """
       The ChronoLink rollout began on May 8, 2023, and progress has been slower than expected due to several complications. The infrastructure team encountered unexpected compatibility issues with the legacy scheduling system, which introduced a four-week delay. 

Additionally, on August 17, 2023, the security group requested an urgent revision to the encryption layer, requiring the engineering teams to reallocate resources. The team has been working consistently, but these adjustments have disrupted the development timeline.

Clients have started requesting updated release estimates, especially after the recent queue-processing failure that affected approximately 3,200 users. A clear, steady communication plan is needed to maintain confidence while the remaining work is completed.

    """

sample_analysis = extract_intent(sample_original)



clean_version = rewrite_with_groq(sample_original, sample_analysis)
human_version = human_imperfection_layer(clean_version,sample_analysis)
final_human = humanize_with_groq(human_version)


print(final_human)

