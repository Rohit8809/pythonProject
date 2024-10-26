# A simple recommendation script

# Sample user data and movie ratings
users = {
    'Alice': {'Movie1': 5, 'Movie2': 3, 'Movie3': 4},
    'Bob': {'Movie1': 4, 'Movie2': 5, 'Movie4': 2},
    'Charlie': {'Movie2': 5, 'Movie3': 3, 'Movie4': 4},
}


def get_recommendations(user):
    user_ratings = users[user]
    recommendations = []

    for other_user, ratings in users.items():
        if other_user != user:  # Avoid comparing with self
            for movie, rating in ratings.items():
                if movie not in user_ratings:  # Check if user has not rated the movie
                    recommendations.append((movie, rating))

    # Sort recommendations by score in descending order
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations


# Example usage
for user in users.keys():
    recommendations = get_recommendations(user)

    # Print output
    print(f"Recommendations for {user}:")
    if recommendations:
        for movie, score in recommendations:
            print(f"Movie: {movie}, Score: {score}")
    else:
        print("No recommendations available.")
    print()  # Print a new line for better readability
