// (SP1) Any user can read the home page
// This is an availability policy and thus not enforceable with Cedar

// (SP2) Authenticated users with the USER role can create thoughts
permit (
principal is User,
action == Action::"createThought",
resource is Thought
) when {
    principal.role == Role::"baseuser"
};


// (SP3) Authenticated users with the USER role can delete their own thoughts
permit (
principal is User,
action == Action::"deleteThought",
resource is Thought
) when {
    principal.role == Role::"baseuser" && resource.creator == principal
};


// (SP4) Authenticated users with the USER role can vote at most three times for the same thought
forbid (
    principal is User,
    action == Action::"createVote",
    resource is Vote
) when {
    resource.thought.votedBy
    -> filter(v => v.voter.uid.id == principal.uid.id)
    -> count() >= 3
};

// OR 

thought
permit (
    principal is Person in Role::"baseuser",
    action == Action::"voteThought",
    resource is Thought
) when {
    context.personalVoteCount < 3   
    // Cedar is not expressive enough to calculate how many times
    // `principal` has voted for `resource`, so this computation
    // must be done in Python. We provide it to Cedar like this
    // to have all the security policies in the same place.
};


// (SP5) Authenticated users with the USER role are not allowed to vote for their own thoughts
forbid (
    principal is Person in Role::"baseuser",
    action == Action::"voteThought",
    resource is Thought
) when {
    resource.creator == principal     // Alternatively, `resource in principal` if the schema
                                    // uses `Thought in Person`
};

// Alternatively, (SP4) and (SP5) can be combined into a single `permit`
// policy as follows:
//permit (
//    principal is Person in Role::"baseuser",
//    action == Action::"voteThought",
//    resource is Thought
//) when {
//    context.personalVoteCount < 3 && resource.creator != principal
//};

