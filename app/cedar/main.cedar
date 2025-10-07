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
    principal.role == Role::"baseuser"
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



// (SP5) Authenticated users with the USER role are not allowed to vote
forbid (
principal is User,
action == Action::"createVote",
resource is Vote
) when {
    principal.role == Role::"baseuser"
};

