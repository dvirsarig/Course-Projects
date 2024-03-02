
#ifndef RECOMMENDATIONSYSTEM_H
#define RECOMMENDATIONSYSTEM_H
#include "User.h"
#include <map>
#include <algorithm>
#define MIN_VALUE (-10)
typedef std::map<sp_movie, std::shared_ptr<std::vector<double>>, equal_func>
movie_map;
class RecommendationSystem
{
 private:
  std::shared_ptr<movie_map> data_system;
  std::size_t num_of_features;
public:
	explicit RecommendationSystem();
    /**
     * adds a new movie to the system
     * @param name name of movie
     * @param year year it was made
     * @param features features for movie
     * @return shared pointer for movie in system
     */
	sp_movie add_movie(const std::string& name,int year,
                       const std::vector<double>& features);


    /**
     * a function that calculates the movie with highest score based on
     * movie features
     * @param ranks user ranking to use for algorithm
     * @return shared pointer to movie in system
     */
	sp_movie recommend_by_content(const User& user);

    /**
     * a function that calculates the movie with highest predicted score
     * based on ranking of other movies
     * @param ranks user ranking to use for algorithm
     * @param k
     * @return shared pointer to movie in system
     */
	sp_movie recommend_by_cf(const User& user, int k);


    /**
     * Predict a user rating for a movie given argument using item cf
     * procedure with k most similar movies.
     * @param user_rankings: ranking to use
     * @param movie: movie to predict
     * @param k:
     * @return score based on algorithm as described in pdf
     */
	double predict_movie_score(const User &user, const sp_movie &movie,
												  int k);

	/**
	 * gets a shared pointer to movie in system
	 * @param name name of movie
	 * @param year year movie was made
	 * @return shared pointer to movie in system
	 */
	sp_movie get_movie(const std::string &name, int year) const;


  friend std::ostream& operator<<(std::ostream& s,
      const RecommendationSystem& movie);

};

// Next function made to calculate of the similtary between two vectors.
double scalar_multiple(std::vector<double>& v1, std::vector<double>& v2);
double nor_vector(std::vector<double>& v);
double similtary_func(std::vector<double>& v1, std::vector<double>& v2);

bool sort_by_double(const std::pair<sp_movie, double>& pair1, const
std::pair<sp_movie , double>& pair2); // Comparator for the maps.

#endif //RECOMMENDATIONSYSTEM_H
