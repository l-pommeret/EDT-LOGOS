import webpack from "webpack";
import type { Configuration as DevServerConfiguration } from "webpack-dev-server";
import path from "path";
import cssnanoPlugin from "cssnano";
import HtmlWebpackPlugin from "html-webpack-plugin";
import ESLintPlugin from "eslint-webpack-plugin";

const config: webpack.Configuration = {
  devServer: {
    hot: true,
    static: {
      directory: path.join(__dirname, "."),
    },
  } as DevServerConfiguration,
  devtool: "source-map",
  entry: {
    // Main Application
    app: "./src/index.tsx",
    // Bare Application (no UI around)
    single: "./src/embed.tsx",
  },
  module: {
    rules: [
      {
        // Loads js and jsx files with babel
        exclude: /(node_modules|bower_components)/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/env", "@babel/preset-react"],
        },
        test: /\.(js|jsx)$/i,
      },
      {
        // Loads ts and tsx files with ts-loader
        exclude: /(node_modules|bower_components)/,
        loader: "ts-loader",
        test: /\.(ts|tsx)$/i,
      },
      {
        // Loads css files with style-loader > css-loader > postcss-loader
        test: /\.css$/i,
        use: [
          "style-loader",
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: [
                  "postcss-preset-env",
                  cssnanoPlugin({ preset: "default" }),
                  "autoprefixer",
                ],
              },
            },
          },
        ],
      },
      {
        // Load images and videos as resources
        test: /\.(png|svg|jpg|jpeg|gif|webp|webm)$/i,
        type: "asset/resource",
      },
      {
        // Load markdown as source
        test: /\.(md|txt)$/i,
        type: "asset/source",
      },
    ],
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },
  },
  output: {
    assetModuleFilename: "static/assets/[name].[hash][ext]",
    clean: true,
    filename: "static/js/[name].[chunkhash].js",
    path: path.resolve(__dirname, "dist"),
    publicPath: process.env["ASSET_PATH"] || "/",
  },
  plugins: [
    // Checks for errors in code
    new ESLintPlugin(),
    // Generates index.html
    new HtmlWebpackPlugin({
      chunks: ["app"],
      filename: "index.html",
      hash: true,
      template: "./src/templates/app.html",
    }),
    // Generates single.html
    new HtmlWebpackPlugin({
      chunks: ["single"],
      filename: "embed.html",
      hash: true,
      template: "./src/templates/embed.html",
    }),
    // Provides the process polyfill
    new webpack.ProvidePlugin({
      process: "process/browser",
    }),
    // Provides the DATA_PATH environment variable
    new webpack.EnvironmentPlugin({
      DATA_PATH: "/data/",
    }),

  ],
  resolve: { extensions: ["*", ".js", ".jsx", ".ts", ".tsx"] },
};
export default config;
