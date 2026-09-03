# Prompt 1 – Generating a multi-dimensional taxonomy

This is the **actual** prompt we use (the Multi-Dimensional Taxonomy Development
Framework, MDTDF), with the domain left blank for you to fill in. Nothing here is
written for the workshop: this is the working document, and it is what produced the
taxonomies behind the RuBase dashboards you have logins for.

**How to use it.** Paste everything below the line into a frontier model
(Claude Opus, GPT-5.x, Gemini Pro – see the model-selection guide). Replace
`{{DOMAIN}}` with your own domain in one sentence. If you have a corpus, paste
20–50 titles and abstracts after the prompt and say *"ground the dimensions in this
corpus, and tell me which dimensions the corpus does NOT support."*

**What good output looks like.** 5–7 dimensions that survive the independence test,
not 15 that overlap. If two of your HLTPs always move together, you have one
dimension wearing two hats – merge them.

**The check that matters.** Before you accept a taxonomy, run the independence test
in the "Testing for Independence" section by hand on three real cases. A model will
happily generate a beautiful taxonomy whose dimensions are not independent, and it
will not tell you.

---

## Multi-Dimensional Taxonomy Development Framework (MDTDF)

**Domain for this run:** `{{DOMAIN}}`

### Concept Overview

A multi-dimensional taxonomy is a framework for analyzing complex domains through
multiple independent analytical perspectives, each representing a fundamental way of
understanding or looking at a subject matter. Unlike traditional hierarchical
taxonomies which organize concepts along a single dimension, multi-dimensional
taxonomies recognize that complex phenomena exist in high-dimensional conceptual
spaces where multiple factors operate simultaneously and independently.

### Core Principles

- **Dimensional Independence:** Each dimension (High-Level Taxonomic Principle or HLTP) represents a truly independent analytical perspective that can vary without necessarily affecting others.
- **Universal Applicability:** Each dimension should be applicable to all instances within the domain being analyzed.
- **Comprehensive Coverage:** The combined dimensions should capture all essential aspects of the phenomenon.
- **Analytical Power:** The framework should reveal insights that would be missed by simpler categorization schemes.
- **Practical Utility:** The taxonomy should bridge theory and practice, supporting both analysis and operational planning.

### Framework Structure

The multi-dimensional taxonomy is organized on four levels:

1. **High-Level Taxonomic Principles (HLTPs):** Fundamental, independent dimensions or "lenses" for analyzing the domain (e.g., Temporal Dimension, Geographical Scope, Power Application)
2. **Second-Level Elements:** Major divisions within each HLTP
3. **Third-Level Elements:** Specific operational areas within each second-level element
4. **Taxa:** Concrete instances or activities that can be classified along all dimensions

### HLTP Development Guidelines

When developing HLTPs, ensure that each dimension:

#### Essential Characteristics

- Represents a truly fundamental aspect of the domain
- Can be applied to any instance within the domain
- Is conceptually distinct from all other dimensions
- Reveals essential rather than superficial features
- Enables meaningful differentiation between instances

#### Testing for Independence

An HLTP is independent if:

- Classification along one dimension does not determine classification along others
- You can find examples where an instance's position on one dimension changes while its position on other dimensions remains constant
- The dimension captures a unique aspect not covered by other dimensions

#### Validation Criteria

Evaluate potential HLTPs against these criteria:

- **Independence:** Does this dimension vary independently of others?
- **Universality:** Can all domain instances be classified along this dimension?
- **Fundamentality:** Does this dimension capture an essential rather than superficial aspect?
- **Distinctiveness:** Does this dimension provide a unique analytical perspective?
- **Utility:** Does this dimension reveal important insights or support practical applications?

### Development Methodology

Follow these steps to build a multi-dimensional taxonomy:

#### Phase 1: Initial Dimension Identification

1. **Domain Definition:** Clearly define the boundaries of what you're analyzing
2. **Brainstorming:** Generate potential dimensions from multiple perspectives
3. **Literature Review:** Identify existing frameworks and dimensions from relevant literature
4. **Expert Consultation:** Gather input from domain specialists
5. **First Principles Analysis:** Consider what fundamental aspects define the domain

#### Phase 2: Dimension Refinement

1. **Independence Testing:** Systematically test each dimension for independence
2. **Classification Exercise:** Attempt to classify diverse examples along each dimension
3. **Gap Analysis:** Identify aspects not captured by current dimensions
4. **Redundancy Elimination:** Merge or remove dimensions that overlap conceptually
5. **Dimension Definition:** Clearly articulate what each dimension represents

#### Phase 3: Second-Level Development

1. **Division Identification:** For each HLTP, identify its major components
2. **Mutual Exclusivity Check:** Ensure categories within an HLTP don't overlap
3. **Completeness Verification:** Ensure categories cover all possibilities within that dimension
4. **Definition Clarification:** Provide clear definitions for each second-level element
5. **Boundary Testing:** Test edge cases to verify category boundaries

#### Phase 4: Testing and Validation

1. **Real-World Testing:** Apply the taxonomy to diverse real-world examples
2. **Edge Case Analysis:** Test the taxonomy against unusual or complex cases
3. **Expert Validation:** Have domain experts review and critique the taxonomy
4. **Practical Application Test:** Use the taxonomy for its intended purpose and evaluate results
5. **Refinement Iteration:** Adjust dimensions and categories based on testing

### Practical Applications

A well-constructed multi-dimensional taxonomy enables:

- **Epistemic MRIs:** When combined with exhaustive corpora and the use of LLMs for first relevance filtering and then classification of semantic text chunks, taxonomies allow for systematic literature reviews
- **Gap Identification:** Locate blind spots in current approaches
- **Comprehensive Assessment:** Evaluate activities across all dimensions
- **Balance Analysis:** Identify over- and under-emphasized areas
- **Comparative Analysis:** Compare different approaches systematically
- **Pattern Recognition:** Identify recurring patterns across dimensions

### Implementation Guidance

#### Starting Points

- Begin with 5-7 clearly independent dimensions
- Focus on dimensions with immediate practical relevance
- Test the framework with familiar examples
- Gather feedback from potential users
- Refine based on initial applications

#### Common Pitfalls to Avoid

- Creating dimensions that are actually different aspects of the same thing
- Developing overly complex frameworks that are difficult to use
- Prioritizing theoretical elegance over practical utility
- Treating the taxonomy as fixed rather than evolving
- Focusing exclusively on familiar or comfortable dimensions

#### Best Practices

- Document dimension definitions thoroughly
- Provide clear examples for each dimension and category
- Create visualization tools to aid understanding
- Develop training materials for users
- Establish a process for ongoing refinement

### Example of Dimensional Analysis

To illustrate how multi-dimensional analysis works, consider a community policing
patrol analyzed through multiple HLTPs:

- **Temporal Dimension:** Pre-incident (preventive activity)
- **Geographical Scope:** Local (neighborhood-level activity)
- **Power Application:** Soft power (influence through presence and relationships)
- **Stakeholder Interaction:** Community engagement (direct public interaction)
- **Process Flow:** Throughput process (ongoing activity rather than input or output)
- **Knowledge Dimension:** Tacit knowledge (relies on experiential understanding)
- **Operational Level:** Tactical (implements strategic direction at field level)

This multi-dimensional analysis reveals aspects that would be missed by simpler
categorizations, showing how the same activity serves multiple functions
simultaneously through different analytical lenses.

### Guidance for Taxonomy Expansion

As your understanding deepens:

- **Extend Dimensions:** Add new dimensions as they become apparent
- **Deepen Categories:** Develop more nuanced sub-categories
- **Create Cross-Dimensional Maps:** Identify how dimensions interact
- **Develop Measurement Tools:** Create ways to assess position along dimensions
- **Build Application Guides:** Create guidance for using the taxonomy in specific contexts

Remember that a taxonomy is a tool for understanding, not an end in itself. The
ultimate test of a multi-dimensional taxonomy is whether it enhances understanding
and supports better decision-making in its domain of application.

### TSV Output Format

Your final output should be structured as a tab-separated value (TSV) file with the
following format:

#### 1. Column Structure

Exactly 4 columns with headers: `HLTP`, `2nd Level TE`, `3rd Level TE`, and `Taxon`

All column values should be separated by tab characters.

#### 2. Content Organization

- **HLTP:** The high-level taxonomic principle (primary dimension)
- **2nd Level TE:** Major category within the HLTP
- **3rd Level TE:** Specific operational area within the 2nd level
- **Taxon:** Concrete instance or specific activity

#### 3. Formatting Requirements

- No quotation marks around values
- No additional columns or metadata
- Consistent capitalization for each HLTP and its elements
- Each row represents one complete classification path
- Group all items by HLTP, then by 2nd Level, then by 3rd Level

#### 4. Example Structure

    HLTP	2nd Level TE	3rd Level TE	Taxon
    Functional Domain	Law Enforcement	Criminal Apprehension	Suspect pursuit and capture
    Functional Domain	Law Enforcement	Criminal Apprehension	Warrant execution
    Functional Domain	Law Enforcement	Evidence Management	Crime scene processing

#### 5. Comprehensiveness

- Each HLTP should have multiple 2nd Level elements
- Each 2nd Level element should have multiple 3rd Level elements
- Each 3rd Level element should have multiple taxa
- Aim for 8-15 concrete taxa for each 3rd Level element
- Ensure completeness of the taxonomy tree

### Instructions for Use

When using this framework to develop a multi-dimensional taxonomy:

1. **Define Your Domain:** Clearly specify what you are creating a taxonomy for
2. **Follow the Methodology:** Work through all four phases systematically
3. **Validate Independence:** Ensure each HLTP is truly independent
4. **Test Thoroughly:** Apply the taxonomy to real-world examples
5. **Output in TSV Format:** Follow the exact structure specified above
6. **Be Comprehensive:** Ensure complete coverage at all levels
7. **Maintain Consistency:** Use consistent terminology and capitalization throughout

Please produce a complete taxonomy following this exact structure, with no
deviations in format.
